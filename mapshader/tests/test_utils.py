import os
import pytest
import shutil

from mapshader.core import render_map
from mapshader.sources import MapSource, elevation_source
from mapshader.utils import get_tiles_in_dir, save_static_tile


TEST_DIR = '.test_utils'


@pytest.fixture
def remove_files():
    if os.path.isdir(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    yield
    if os.path.isdir(TEST_DIR):
        shutil.rmtree(TEST_DIR)


def test_get_tiles_in_dir(remove_files):
    os.mkdir(TEST_DIR)
    os.mkdir(TEST_DIR+'/1')
    os.mkdir(TEST_DIR+'/1/2')
    open(TEST_DIR+'/1/2/2', 'w').close()
    open(TEST_DIR+'/1/3', 'w').close()
    os.mkdir(TEST_DIR+'/2')
    os.mkdir(TEST_DIR+'/2/2')

    result = get_tiles_in_dir(TEST_DIR)

    assert len(result) == 2
    assert TEST_DIR+'/1/2/2' in result
    assert TEST_DIR+'/1/3' in result


def test_save_static_tile(remove_files):
    TEST_DIR = '.test_utils'
    source = MapSource.from_obj(elevation_source()).load()
    tile = render_map(source, x=10, y=11, z=8)

    save_static_tile(tile, TEST_DIR + '/8/10/11')
    result = get_tiles_in_dir(TEST_DIR)
    assert len(result) == 1
    assert TEST_DIR + '/8/10/11' in result
