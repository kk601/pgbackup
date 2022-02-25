import pytest
import tempfile

from pgbackup import storage

@pytest.fixture
def infile():
    f = tempfile.TemporaryFile()
    f.write(b'Testing')
    f.seek(0)
    return f

def test_storing_file_locally(infile):
    """
    Writes content from one file-like to another
    """

    outfile = tempfile.NamedTemporaryFile(delete=False)
    storage.local(infile, outfile)
    with open(outfile.name,'rb') as f:
        assert f.read() == b'Testing'

def test_storing_file_on_s3(mocker,infile):
    """
    Writes content from one file-like to S3
    """
    client = mocker.Mock()
    
    storage.s3(client, infile,"bucket","file-name")

    client.upload_fileobj.assert_called_with(infile,"bucket","file-name")

def test_storing_file_on_azure(mocker,infile):
    """
    Writes content from one file-like to azure blob storage container
    """
    blob_client = mocker.Mock()

    storage.azure(blob_client,'data')

    blob_client.upload_blob.assert_called_with('data')
