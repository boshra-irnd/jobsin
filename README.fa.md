# جابسین
___
## _ برای سایت کاریابی API یک _

این پروژه برای ارائه به عنوان نمونه کار با زبان برنامه نویسی python و DjangoRestframework انجام شده است
![alt text](https://miro.medium.com/max/700/1*kR89JbQQK9aAkNVyxE63pg.png)

> Django REST framework is an open source, flexible and fully-featured library  with modular and customizable architecture that aims at building sophisticated  web APIs and uses Python and Django.

## مراجع دیگر
___
[مستندات به زبان انگلیسی](https://github.com/boshra-irnd/jobsin/blob/master/README.mdd)




## کارفرما
___
کارفرما میتواند با استفاده از نام کاربری و رمز عبور ثبت نام کرده و وارد شود.
و
- موقعیت های شغلی را ایجاد کند
- اطلاعات کارجویانی که برای موقعیت شغلی تعریف شده توسط کارفرما درخواست فرستاده اند را ببیند
- وضعیت درخواست کارجویان را به یکی از چهار مورد درحال بررسی یا رد شده یا مصاحبه و یا استخدام تغییر بدهند

## کارجو
___
کارجو میتواند با استفاده از نام کاربری و رمزعبور ثبت نام کرده و وارد شود
و
- آگهی های ثبت شده توسط کارفرماها را ببینند
- اطلاعات شرکت استخدام کننده را ببینند
- برای کارفرما درخواست ارسال کنند

## پکیج های استفاده شده

- Python 3.8.10 
- DjangoRestFramework 3.13.1
- DjangoRestFramework-Simplejwt 5.1.0

## راه اندازی

ubuntu 20.04 برای  این مراحل را طی کنید 


این موارد نصب شوند:
- git 
- postgresql 
- python3
- python3-dev 
- python3-venv


محیط مجازی با این دستور ایجاد شود

```
python3 -m venv my_env
```
محیط مجازی با این دستورات فعال شود
```
source my_env/bin/activate
```
نصب کردن موارد موردنیاز
```
pip install -r requirements.txt
```
و باید یک فایل به اسم dev.py در آدرس jobsen/settings ایجاد کنید و SECRET_KEY و DATABASES را در آن تعریف کنید.
