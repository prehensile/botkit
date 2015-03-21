import logging, sys

def init_logging( root_level=logging.DEBUG,
                     stdout_level=logging.DEBUG,
                     pth_logfile=None,
                     logfile_level=logging.DEBUG ):
    
    # set root log level
    root = logging.getLogger()
    root.setLevel( root_level )
    
    fmt = logging.Formatter('%(asctime)s [%(levelname)s][%(filename)s: %(lineno)d] %(message)s')

    # set up & add handler for stdout
    ch = logging.StreamHandler( sys.stdout )
    ch.setLevel( stdout_level )
    ch.setFormatter( fmt )
    root.addHandler( ch )

    # set up & add file logger
    if pth_logfile is not None:
        fh = logging.FileHandler( pth_logfile )
        fh.setLevel( logfile_level )
        fh.setFormatter( fmt )
        root.addHandler( fh )