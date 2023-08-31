from __future__ import print_function
import csv, os
import requests
from PIL import Image
import multiprocessing


def url_to_image(url):
    img = Image.open(requests.get(url, stream=True, verify=False).raw)
    return img

# chain,hotel,im_source,im_id,im_url
def download_and_resize(imList):
    for im in imList:
        saveDir = os.path.join('./images/train/',im[0],im[1],im[2])
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)

        savePath = os.path.join(saveDir,str(im[3])+'.png')

        if not os.path.isfile(savePath):
            img = url_to_image(im[4])
            if img.size[1] > img.size[0]:
                width = 640
                height = round((640 * img.size[0]) / img.size[1])
                img = img.resize((width, height))
            else:
                height = 640
                width = round((640 * img.size[1]) / img.size[0])
                img = img.resize((width, height))
            img.save(savePath)
            print('Good: ' + savePath)
        else:
            print('Already saved: ' + savePath)


def main():
    hotel_f = open('./input/dataset/hotel_info.csv','r')
    hotel_reader = csv.reader(hotel_f)
    hotel_headers = next(hotel_reader,None)
    hotel_to_chain = {}
    for row in hotel_reader:
        hotel_to_chain[row[0]] = row[2]

    train_f = open('./input/dataset/train_set.csv','r')
    train_reader = csv.reader(train_f)
    train_headers = next(train_reader,None)

    images = []
    for im in train_reader:
        im_id = im[0]
        im_url = im[2]
        im_source = im[3]
        hotel = im[1]
        chain = hotel_to_chain[hotel]
        images.append((chain,hotel,im_source,im_id,im_url))

	
    pool = multiprocessing.Pool()
    NUM_THREADS = multiprocessing.cpu_count()
    
    for cpu in range(NUM_THREADS):
        pool.apply_async(download_and_resize,[images[cpu::NUM_THREADS]])
    pool.close()
    pool.join()


if __name__ == '__main__':
    retcode = main()