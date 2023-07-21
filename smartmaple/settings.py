

BOT_NAME = "smartmaple"

SPIDER_MODULES = ["smartmaple.spiders"]
NEWSPIDER_MODULE = "smartmaple.spiders"

ITEM_PIPELINES = {
   'smartmaple.pipelines.MongoPipeline': 300,
}

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'smartmaple'
