import click
import logging
from .builder import generate_from_configuration, question_csv
from .utils import calculate_query_length, merge_dir_csvs


@click.group()
def cli():
    """serverless-survey: build and manage serverless survey HTML files."""
    pass


@cli.command('generate')
@click.option('-f', '--config-file',
              help='Path to YAML configuration file (default: configuration.yml)')
@click.option('-p', '--out-rel-path', default='',
              help='Output directory for generated HTML files')
@click.option('-r', '--repo-name',
              help='Repository name for building GitHub Pages URL')
@click.option('-g', '--gh-org',
              help='GitHub organization or user that owns the repo')
@click.option('-u', '--out-url',
              help='Full base URL of the hosted site (overrides --repo-name / --gh-org)')
@click.option('-d', '--debug', is_flag=True,
              help='Print debug information')
@click.option('--fragment', is_flag=True,
              help='Generate HTML fragment instead of full page')
@click.option('-a', '--all-in-one', is_flag=True,
              help='Merge all pages into a single aio.html file')
@click.option('-t', '--pass-through', multiple=True, default=['id'],
              help='Variable to pass through all questions (repeat for multiple, default: id)')
@click.option('-i', '--instructions-type', default='forward',
              type=click.Choice(['log', 'forward', 'minimal', 'blank'], case_sensitive=False),
              help='Format for the generated instructions markdown file')
def generate(config_file, out_rel_path, repo_name, gh_org, out_url, debug, fragment,
             all_in_one, pass_through, instructions_type):
    """Generate HTML survey files from a YAML configuration file."""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    generate_from_configuration(
        config_file=config_file,
        out_rel_path=out_rel_path,
        repo_name=repo_name,
        gh_org=gh_org,
        out_url=out_url,
        debug=debug,
        fragment=fragment,
        all_in_one=all_in_one,
        study_pass_through_vars=list(pass_through),
        instructions_type=instructions_type,
    )


@cli.command('check')
@click.argument('filename', type=click.Path(exists=True))
@click.option('-V', '--vars-only', is_flag=True, default=False,
              help='Count variables and joiners only, excluding prefix and assumed value lengths')
@click.option('-i', '--id-length', type=int, default=10,
              help='Length of unique identifier in characters (default: 10)')
@click.option('-l', '--value-length', type=int, default=3,
              help='Average length in characters of non-id values (default: 3)')
@click.option('-b', '--exclude-base', is_flag=True,
              help='Exclude the base URL from the character count')
def check(filename, vars_only, id_length, value_length, exclude_base):
    """Check the estimated query string length from an instructions file."""
    est_chars = calculate_query_length(filename, vars_only, id_length, value_length, exclude_base)
    if est_chars > 2000:
        click.secho(
            f'Warning: {est_chars} estimated characters — recommended limit is 2000',
            fg='yellow'
        )
    else:
        click.echo(f'Estimated message length is safe at {est_chars} characters')


@cli.command('merge')
@click.argument('folder', type=click.Path(exists=True))
@click.option('-m', '--merge-on', default=['id'], multiple=True,
              help='Column to merge on — repeat for multiple columns (default: id)')
@click.option('-h', '--header', default=0,
              help='Row number to use as the header, starting from 0 (default: 0)')
@click.option('-s', '--skip-row', multiple=True, type=int, default=[1, 2],
              help='Row number to skip — repeat for multiple rows (default: 1 2)')
@click.option('-o', '--out-name', default=None,
              help='Output CSV filename — defaults to folder name')
@click.option('-v', '--verbose', is_flag=True,
              help='Print progress details')
@click.option('-c', '--complete-only', is_flag=True,
              help='Keep only rows present in all files (inner merge; default is outer)')
def merge(folder, merge_on, header, skip_row, out_name, verbose, complete_only):
    """Merge all CSV files in a folder into a single CSV."""
    if verbose:
        logging.basicConfig(level=logging.INFO)
    out_name = merge_dir_csvs(folder, merge_on, out_name, header, verbose, skip_row, complete_only)
    click.echo(f'Wrote merged CSV to {out_name}')


@cli.command('metadata')
@click.option('-f', '--config-file',
              help='Path to YAML configuration file')
@click.option('-m', '--metadata', multiple=True, default=None,
              help='Metadata field to include as a column (repeat for multiple)')
def metadata(config_file, metadata):
    """Export question metadata from a configuration file to CSV."""
    csv_file = question_csv(config_file=config_file, metadata=metadata or None)
    click.echo(f'Wrote metadata to {csv_file}')


# Backward-compatible aliases (kept so existing scripts and docs still work)
generate_from_configuration = generate
check_query_length = check
cmd_merge_dir_csvs = merge
question_csv_cmd = metadata
