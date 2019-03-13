# Generated by Django 2.1.7 on 2019-03-12 16:10

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0010_auto_20190121_0157'),
    ]

    operations = [
        migrations.CreateModel(
            name='Popup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='제목')),
                ('is_active', models.BooleanField(default=False, verbose_name='활성화 여부')),
                ('pos_x', models.CharField(default='50px', max_length=100, verbose_name='팝업 가로 위치')),
                ('pos_y', models.CharField(default='100px', max_length=100, verbose_name='팝업 세로 위치')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, help_text='팝업 내용을 직접 작성하는 경우 입력', null=True, verbose_name='팝업 내용')),
                ('image', models.ImageField(blank=True, help_text='설정시 팝업 내용은 이미지로 채워집니다.', null=True, upload_to='popup', verbose_name='이미지 팝업')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='생성일')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='page.Page', verbose_name='표출 할 페이지')),
            ],
            options={
                'verbose_name': '팝업창',
                'verbose_name_plural': '팝업창 목록',
            },
        ),
    ]
