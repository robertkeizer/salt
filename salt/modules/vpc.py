'''
Amazon VPC Module
'''
import logging
import inspect
import re
import sys
import boto
import boto.vpc

log = logging.getLogger(__name__)

__func_alias__ = { }

def __virtual__( ):
    return 'vpc'

def _get_connection( ):
    '''
    Helper method to handle creation of the actual
    boto.vpc.VPCConnection object. This uses
    configuration values from salt.

    Also checks if one already exists.
    '''

    # Just a placeholder for now. ( Dummy values to simply trick boto into 
    # not throwing an exception ).
    return boto.vpc.VPCConnection( "foo", "bar" )

def _create_func( function_name, function_obj ):
    '''
    Create a python function that is directly based on
    function_obj. Note that introspection is used to do this.
    '''

    # Get the documentation from the object.
    doc = inspect.getdoc( function_obj )

    # Get the signature of the function.
    spec = inspect.getargspec( function_obj )

    # Define the actual function we will return.
    def _f( *args ):
        '''
        Todo.
        '''
        # Use spec to reconcile what we get from *args
        # and call the boto function.

        # getattr( _get_connection( ), function_name ) is the actual boto obj.

        pass

    return _f

# Iterate over the boto object. Note that we're using an instance not a class
# because inspect.isfunction checks if the function is bound or not.
for member_name, member_method in inspect.getmembers( _get_connection( ) ):

    # We only want methods.
    if not inspect.ismethod( member_method ):
        continue

    # Blacklist __ functions..
    if re.compile( "^__" ).match( member_name ):
        continue

    # Call _create_func with the particular member name and function.
    # Then set it to be class wide. Note that we append of suffix
    # of '_' to methods that are generated out of _create_func.

    setattr(
            sys.modules[__name__],
            '{0}_'.format( member_name ),
            _create_func( member_name, member_method )
    )

    # Update func alias so that salt finds the new function.
    __func_alias__['{0}_'.format( member_name )] = member_name
