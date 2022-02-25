def local(infile,outfile):
    outfile.write(infile.read())
    outfile.close()
    infile.close()

def s3(client, infile, bucket, filename):
    client.upload_fileobj(infile,bucket,filename)

def azure(blob_client,data):
    blob_client.upload_blob(data)