# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from time import localtime
from scrapy import Request
import hashlib
from scrapy.utils.python import to_bytes

from .models import *

def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path

class XiachufangImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)
        ## end of deprecation warning block
        datefolder = str(localtime().tm_year) + str(localtime().tm_mon)
        image_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return '%s/%s.jpg' % (datefolder,image_guid)

    def thumb_path(self, request, thumb_id, response=None, info=None):
        ## start of deprecation warning block (can be removed in the future)
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.thumb_key(url) method is deprecated, please use '
                          'thumb_path(request, thumb_id, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from thumb_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if thumb_key() method has been overridden
        if not hasattr(self.thumb_key, '_base'):
            _warn()
            return self.thumb_key(url, thumb_id)
        ## end of deprecation warning block
        datefolder = str(localtime().tm_year) + str(localtime().tm_mon)
        thumb_guid = hashlib.sha1(to_bytes(url)).hexdigest()  # change to request.url after deprecation
        return '%s/thumbs/%s/%s.jpg' % (datefolder,thumb_id, thumb_guid)

class Xiachufang2Pipeline(object):
    def process_item(self, item, spider):
        data=Recipe(
            food=item['title'],
            step=item['steps'],
            tip=item['tip'],
            description=item['description']
        )
        session.add(data)
        session.commit()

        for k,v in list(item['stuff'].items()):
            mat=Material(
                material=k,
                volume=v
            )
            mat.foods=[data]
            session.add(mat)
            session.commit()

    # id=Column(Integer,autoincrement=True,primary_key=True)
    # food=Column(String(128),nullable=False)
    # step=Column(Text)
    # tip=Column(Text)
    # description=Column(Text)
    # materials=relationship('Material',secondary=Recipe_Mat)

    # material = Column(String(128), nullable=False)
    # volume=Column(String(128))
    # foods = relationship('Recipe', secondary=Recipe_Mat)


    # description=scrapy.Field()
    # tip=scrapy.Field()
    # stuff=scrapy.Field()
    # title = scrapy.Field()
    # steps = scrapy.Field()
    # image_urls = scrapy.Field()
    # image_paths = scrapy.Field()


















