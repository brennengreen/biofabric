import glob
import os

# list available backends
__backends = {}
for fn in glob.glob(os.path.join(os.path.dirname(__file__), "*_backend.py")):
    fn = os.path.basename(fn)
    __backends[fn[:-11]] = fn[:-3]


def draw(graph, filename, output_format=None, backend="pyx", **kwargs):
    """ Draw a network using the BioFabric layout technique

       Arguments:
           graph			(mandatory) network to draw, as a NetworkX object
           filename		(mandatory) name of the output file
           output_format 	(optional) format of the output file. If not provided, the format will be infered from the extension of 'filename'
           backend 		(optional) backend to generate the output file. If not provided, the default PyX backend will be selected

       Additional keyword arguments will be sent to the backend. See the backend-specific documentation.
    """
    if backend in __backends:
        backend_ = __import__(__backends[backend], globals())
    else:
        raise ValueError("unknown backend '%s'" % backend)

    if output_format is None:
        if '.' not in filename:
            raise Exception("unable to infer output format from filename '%s'" % filename)
        output_format = filename.rsplit('.', 1)[1].lower()

    if output_format not in backend_.accepted_formats:
        raise ValueError("backend %s doesn't support %s format" % (backend, output_format))

    return backend_.draw(graph, filename, output_format, kwargs)
