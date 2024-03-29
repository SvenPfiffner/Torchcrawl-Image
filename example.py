import torchcrawl_image as tci

# Crawl a website
#crawler = tci.Crawler("./data", force_overwrite=True)
#crawler.crawl("https://en.wikipedia.org/wiki/Bee")

# Create a dataset
dataset = tci.TorchcrawlDataset("./data")
tci.gui.run(dataset)