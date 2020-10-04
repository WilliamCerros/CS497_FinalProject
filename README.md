# Rock_GAN

Program Description: This program will download ~8,000 images of rock climbing locations from the website http://www.myfirstascent.com/app/routes.
                     Main.py serves as the web crawler which will navigate through the website and download every image available. After downloading these images
                     the web crawler will also download the satelite image view of each rock by accessing the coordinates associated with each picture through the JSON data
                     available on the image's webpage. By using the google maps API we are able to view the satelite image of each rock by using the coordinates from our JSON data. 
                     This will create two datasets of ~8,000 images each. The file CS497_Final.ipynb serves as the Generative Adversarial model which will train on the two
                     datasets and synthesize a fake image that resembles the images from each dataset.  
