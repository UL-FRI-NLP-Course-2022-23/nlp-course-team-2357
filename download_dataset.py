import os
import urllib.request as req
import zipfile
import gzip


XML = "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1034/cckresV1_0.zip?sequence=1&isAllowed=y"
TEXT = "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1034/cckresV1_0-text.zip?sequence=4&isAllowed=y"
VERT = "https://www.clarin.si/repository/xmlui/bitstream/handle/11356/1034/cckres.vert.gz?sequence=3&isAllowed=y"


def download(data_dir, zip_name, url):

    # Download the zip to a temporary file
    print(f"Downloading to {zip_name}.zip...")
    temp_zip_path = os.path.join(data_dir, f"{zip_name}.zip")
    req.urlretrieve(url, temp_zip_path)

    # Extract and rename folder
    print("Extracting...")
    with zipfile.ZipFile(temp_zip_path, "r") as z:
        folder_name = z.namelist()[0].split("/")[0]  # cckresV1_0 or cckresV1_0-text
        data_path = os.path.join(data_dir, zip_name)
        z.extractall(data_dir)
        os.rename(os.path.join(data_dir, folder_name), data_path)

    # Remove the temporary file
    os.remove(temp_zip_path)

    print(f"Successfully downloaded into {data_path}.\n")


def download_vert(data_dir):
    # Download the gzip to a temporary file
    file_name = "cckres.vert"
    print(f"Downloading to {file_name}.gz...")
    temp_zip_path = os.path.join(data_dir, f"{file_name}.gz")
    req.urlretrieve(VERT, temp_zip_path)

    # Save cckres.vert from cckres.vert.gz, into the file with same name
    # https://www.tutorialspoint.com/python-support-for-gzip-files-gzip
    print("Extracting...")
    with gzip.open(temp_zip_path, "rb") as z:
        content = z.read()
        data_path = os.path.join(data_dir, "vert")
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        with open(os.path.join(data_path, file_name), "wb") as out:
            out.write(content)

    # Remove the temporary file
    os.remove(temp_zip_path)

    print(f"Successfully downloaded into {data_path}.\n")


def main():
    data_dir = "cckres"
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    download(data_dir, "xml", XML)
    download(data_dir, "text", TEXT)
    download_vert(data_dir)


if __name__ == "__main__":
    main()
