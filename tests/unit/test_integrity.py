import os
from subprocess import call


ROOT = os.path.normpath(
    os.path.join(
      os.path.dirname(__file__),
      os.pardir,
      os.pardir,
      'meetup'
    )
)


def find_files(root, extensions):
    matches = []
    for root, _, filenames in os.walk(root):
        for filename in filenames:
            if any(filename.endswith(e) for e in extensions):
                matches.append(os.path.join(root, filename))
    return matches


def test_codebase():
    '''
    grep all codebase looking for invalid strings
    '''
    string_error = [
        ('<<<<<<<', 'Merge conflict'),
        ('pdb.set_trace', 'pdb trace'),
    ]
    kwargs = {
        'stdout': open('/dev/null', 'a'),
        'stderr': open('/dev/null', 'a'),
    }
    for filename in find_files(ROOT, ['.py', '.js', '.html']):
        for string, error_msg in string_error:
            assert call(['grep', string, filename], **kwargs), (
              "%s %r in %s" % (error_msg, string, filename[len(ROOT) - 5:])
            )
