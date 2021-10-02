# 🤖 AI-workflow
Using MATLAB & Python

**Content:**
1. [Access data](#access)
2. [Prepare data](#prepare)
3. [Train model](#train)
4. [Test model](#test)


![gta](img/videoPlayer-full-view.gif)

## 1. <a name="access"></a>Access data


**Get images and controller data**

```matlab
training_dataset = "2021-03-06-1";
i = 1;
training_img = imread("D:\devel\AI-workflow\samples2\"+training_dataset+"\img_"+string(i)+".png");
imshow(training_img)
```

![figure_1.png](img/figure_1.png)


```matlab
data = readtable("D:\devel\AI-workflow\samples2\"+training_dataset+"\data.csv");
data = renamevars(data,["Var1","Var2","Var3","Var4","Var5","Var6"],["img", "x", "y", "r", "l", "b"]);
data
```

| |img|x|y|r|l|b|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|1|'samples/2021-03-06-...|-0.0157|-0.0079|0|0|0|
|2|'samples/2021-03-06-...|-0.0157|-0.0157|0|0|0|
|3|'samples/2021-03-06-...|-0.0157|-0.0079|0|0|0|
|4|'samples/2021-03-06-...|-0.0157|-0.0079|0|0|0|
|5|'samples/2021-03-06-...|-0.0236|-0.0079|0|0|0|
|6|'samples/2021-03-06-...|-0.0157|-0.0079|0|0|0|
|7|'samples/2021-03-06-...|-0.0157|-0.0079|0|0|0|
|8|'samples/2021-03-06-...|-0.0157|-0.0079|0|0|0|
|9|'samples/2021-03-06-...|-0.0157|-0.0157|0|0|0|
|10|'samples/2021-03-06-...|-0.0157|-0.0079|0.9961|0|0|


```matlab
plot(data.x)
```

![figure_2.png](img/figure_2.png)

**Record from video game**

![record_samples](img/record_samples.png)

*Controller class update* [utils.py](1_access_data/utils.py)
```python
# GTA/Need for Speed
    def read(self):
        x = self.LeftJoystickX
        r = self.RightTrigger
        l = self.LeftTrigger
        a = self.A
        b = self.Y
        return [x, r, l, a, b]
```
## 2. <a name="prepare"></a>Prepare data

Run `python utils.py prepare samples/*` with an array of sample directories to build an `X` and `y` matrix for training. (zsh will expand samples/* to all the directories. Passing a glob directly also works)

`X` is a 3-Dimensional array of images

`y` is the expected joystick ouput as an array:

```
  [0] joystick x axis
  [1] button r
  [2] button l
  [3] button a
  [4] button b
```

*(GTA/Need For Speed Config)*

**Dataset browsing apps**

*(Previous records of Rocket League have a different controller config)*
![matlab_app](img/matlab_desktop_app_rocket.png)

![streamlit_app](img/streamlit_app_nfs.png)

![streamlit_app2](img/streamlit_app_unity.png)


## 3. <a name="train"></a>Train model 

The Deep Learning model used is the one from NVIDIA in this famous [paper](https://arxiv.org/pdf/1604.07316.pdf) from 2016:
![nvidia_network](img/nvidia_network.png)

**MATLAB Deep Learning toolbox**

![matlab_deep_learning](img/matlab_deep_learning.png)


## 4. <a name="test"></a>Test model

**Test pre-trained vehicle detector using [aggregate channel features](https://fr.mathworks.com/help/driving/ref/vehicledetectoracf.html)**

```matlab
detector = vehicleDetectorACF('full-view'); 
% use front-rear-view on highway scenario
vp = vision.VideoPlayer ;

reset(imds);
reset(vp)
while hasdata( imds )
    I = read( imds );
    [bboxes,scores] = detect(detector,I);
    if ~isempty( bboxes )
        I = insertObjectAnnotation(I,'rectangle',bboxes,scores);
    end
    step( vp, I )
    drawnow
end 
```

![figure_3.png](img/figure_3.png)

**Test model trained on supervised dataset**

| |img|x|y|r2|l2|r1|
|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
|1|'samples/2021-03-06-1/img_0.png|-0.015747|-0.023621|0.000000|0.0|0|

![test](img/2021-03-06-1_img_0.png)

```python
>>> joystick = model.predict(vec, batch_size=1)[0]
>>> print(joystick[0])
-0.007983289
```

## Sources
Based on:
* [TensorKart](https://github.com/kevinhughes27/TensorKart)
* [marioKartAI](https://github.com/slevin48/marioKartAI): 🤖AI plays Mario Kart 🏎️
* [gta](https://github.com/slevin48/gta): 🤖 Train a self-driving car in GTA V 🚗
* [rocket](https://github.com/slevin48/rocket): 🚀 AI plays Rocket League ⚽ 🏎️