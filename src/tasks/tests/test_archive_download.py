import os
import tempfile

import numpy as np
import sigmf.sigmffile
from rest_framework import status

import sensor.settings
from tasks.tests.utils import (
    HTTPS_KWARG,
    reverse_archive,
    reverse_archive_all,
    simulate_acquisitions,
    simulate_multirec_acquisition,
)


def test_single_acquisition_archive_download(user_client, test_scheduler):
    entry_name = simulate_acquisitions(user_client, n=1)
    task_id = 1
    url = reverse_archive(entry_name, task_id)
    disposition = 'attachment; filename="{}_test_acq_1.sigmf"'
    disposition = disposition.format(sensor.settings.FQDN)
    response = user_client.get(url, **HTTPS_KWARG)

    assert response.status_code == status.HTTP_200_OK
    assert response["content-disposition"] == disposition
    assert response["content-type"] == "application/x-tar"

    with tempfile.NamedTemporaryFile() as tf:
        for content in response.streaming_content:
            tf.write(content)

        sigmf_archive_contents = sigmf.sigmffile.fromarchive(tf.name)
        md = sigmf_archive_contents._metadata
        datafile = sigmf_archive_contents.data_file
        datafile_actual_size = os.stat(datafile).st_size
        claimed_sha512 = md["global"]["core:sha512"]
        number_of_sample_arrays = len(md["annotations"])
        samples_per_array = md["annotations"][0]["core:sample_count"]
        sample_array_size = samples_per_array * np.float32(0.0).nbytes
        datafile_expected_size = number_of_sample_arrays * sample_array_size
        actual_sha512 = sigmf.sigmf_hash.calculate_sha512(datafile)

        assert datafile_actual_size == datafile_expected_size
        assert claimed_sha512 == actual_sha512


def test_multirec_acquisition_archive_download(user_client, test_scheduler):
    entry_name = simulate_multirec_acquisition(user_client)
    task_id = 1
    url = reverse_archive(entry_name, task_id)
    disposition = 'attachment; filename="{}_test_multirec_acq_1.sigmf"'
    disposition = disposition.format(sensor.settings.FQDN)
    response = user_client.get(url, **HTTPS_KWARG)

    assert response.status_code == status.HTTP_200_OK
    assert response["content-disposition"] == disposition
    assert response["content-type"] == "application/x-tar"

    with tempfile.NamedTemporaryFile() as tf:
        for content in response.streaming_content:
            tf.write(content)

        sigmf_archive_contents = sigmf.archive.extract(tf.name)
        assert len(sigmf_archive_contents) == 3


def test_all_acquisitions_archive_download(user_client, test_scheduler):
    entry_name = simulate_acquisitions(user_client, n=3)
    url = reverse_archive_all(entry_name)
    disposition = 'attachment; filename="{}_test_multiple_acq.sigmf"'
    disposition = disposition.format(sensor.settings.FQDN)
    response = user_client.get(url, **HTTPS_KWARG)

    assert response.status_code == status.HTTP_200_OK
    assert response["content-disposition"] == disposition
    assert response["content-type"] == "application/x-tar"

    with tempfile.NamedTemporaryFile() as tf:
        for content in response.streaming_content:
            tf.write(content)

        sigmf_archive_contents = sigmf.archive.extract(tf.name)
        assert len(sigmf_archive_contents) == 3
