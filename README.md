# Project-ECUST-CourseInfo

## 本地运行代码

1. 切换到 Python3 环境，可以用虚拟环境 virtualenv，总之要确认 `python --version` 的输出是 `Python3` 字样

	```console
	$ python --version
	Python 3.7.3
	$ pip --version
	pip 19.3.1 from /usr/local/lib/python3.7/site-packages/pip (python 3.7)
	```

1. 切换回本项目的根目录，安装 pip 依赖

	```console
	$ ls
	Dockerfile    README.md     ansible-u1804 courseinfo    docker-config  requirements.txt

	$ pip install -r requirements.txt
	```

1. 切换到 courseinfo 目录，初始化数据库

	```console
	$ ls
	README.md        courseinfo       excel            locale           myAPI            static
	classroom        data             initdb.py        manage.py        templates        static_common
	$ python manage.py migrate
	$ python manage.py flush --noinput
	$ python initdb.py
	```

1. 运行站点，浏览器访问：`http://127.0.0.1:8000/`

	```console
	$ python manage.py runserver
	...
	Starting development server at http://127.0.0.1:8000/
	Quit the server with CONTROL-C.
	```

## 制作 Docker 镜像

1. 确认本地 Docker Daemon 正常运行

	```console
	$ docker run hello-world

	Hello from Docker!
	...
	```

1. 切换回本项目的根目录，确认目录中包含 Dockerfile 文件，**注意：`auser/djangodemo` 中的 auser 是你 dockerhub 的账户名**

	```console
	$ ls
	Dockerfile    README.md     ansible-u1804 courseinfo    docker-config  requirements.txt

	$ docker build -t auser/djangodemo .
	Sending build context to Docker daemon  21.11MB
	Step 1/20 : FROM maodouzi/django:v2.2.6
	 ---> 0e1a814c3248
	Step 2/20 : LABEL purpose='ECUST Course Search'
	 ---> Using cache
	 ---> bff5922c57b5
	Step 3/20 : RUN mkdir -p /home/www/ecustCourseInfo/logs
	 ---> Using cache
	 ---> bffb926b0f6d
	...
	Step 20/20 : CMD [ "sh", "/tmp/start.sh" ]
	 ---> Running in 25bedf25c059
	Removing intermediate container 25bedf25c059
	 ---> 52c793bdcd5a
	Successfully built 52c793bdcd5a
	Successfully tagged auser/djangodemo:latest
	```

1. 切换到 courseinfo 目录，在本地测试和运行 Docker 镜像，然后在浏览器上访问: `http://localhost`

	```console
	$ ls
	README.md        courseinfo       excel            locale           myAPI            static
	classroom        data             initdb.py        manage.py        static_common    templates

	$ docker run -d -p 80:80 --mount type=bind,source=$(pwd)/data,target=/home/www/ecustCourseInfo/src/courseinfo/data auser/djangodemo:latest
	221fc877103e55b6a452e8d69838232e122a357972aa08ac4421212395b892bf
	```

1. 停止 Docker 镜像

	```console
	docker stop 221fc877103e55b6a452e8d69838232e122a357972aa08ac4421212395b892bf
	```

1. 镜像上传到 Docker hub

	```bash
	docker login
	docker push auser/djangodemo:latest
	```

## 部署到远端站点

1. 配置 ~/.ssh/config 文件，HostName 可以直接写 IP 地址，IdentityFile 是密钥文件，可以用 ssh-keygen 生成，然后通过 ssh-copy-id 拷贝到远端机器上取。

	```
	Host course
	    HostName        demo-course-search.trystack.cn
	    User            root
	    IdentityFile    ~/.ssh/id_rsa_test
	```

	```console
	$ ssh-keygen
	Generating public/private rsa key pair.
	Enter file in which to save the key (/Users/wuwenxiang/.ssh/id_rsa): /Users/wuwenxiang/.ssh/id_rsa_test
	Enter passphrase (empty for no passphrase):
	Enter same passphrase again:
	Your identification has been saved in /Users/wuwenxiang/.ssh/id_rsa_test.
	Your public key has been saved in /Users/wuwenxiang/.ssh/id_rsa_test.pub.
	The key fingerprint is:
	SHA256:InvociMYhpxxK+FObSyvLYKDA5+GW3SYckqEHyrhbZY wuwenxiang@wuwenxiangdembp
	The key's randomart image is:
	+---[RSA 2048]----+
	|                 |
	|.                |
	|o..              |
	|o*.=.            |
	|Bo&E+ . S        |
	|*&o* + .         |
	|O=*.o .          |
	|O+Boo.           |
	|o*o=..           |
	+----[SHA256]-----+

	$ ssh-copy-id root@demo-course-search.trystack.cn -i ~/.ssh/id_rsa_test.pub
	/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/Users/wuwenxiang/.ssh/id_rsa_test.pub"
	/usr/bin/ssh-copy-id: INFO: attempting to log in with the new key(s), to filter out any that are already installed
	/usr/bin/ssh-copy-id: INFO: 1 key(s) remain to be installed -- if you are prompted now it is to install the new keys

	Number of key(s) added:        1

	Now try logging into the machine, with:   "ssh 'root@demo-course-search.trystack.cn'"
	and check to make sure that only the key(s) you wanted were added.
	```

1. 确认能不用用户名密码，直接访问远端机器

	```console
	$ ssh course
	Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-52-generic x86_64)
	...
	Last login: Wed Nov  6 18:47:17 2019 from 116.238.98.242
	```

1. 切换到 ansible-u1804目录，复制 `inventory/inventory.ini.example`，并修改 webserver 的名字

	```console
	$ ls
	README.md inventory playbooks

	$ cp inventory/inventory.ini.example inventory/inventory.ini

	$ cat inventory/inventory.ini
	[all:vars]
	image_name="auser/djangodemo"

	[webserver]
	course
	```

1. 执行部署

	```console
	$ ansible-playbook -i inventory/inventory.ini playbooks/deploy.yml

	PLAY [webserver] *****************************************************************************************************************

	TASK [Gathering Facts] ***********************************************************************************************************
	ok: [course]

	TASK [init01_pre_install : apt-get update] ***************************************************************************************

	...
	```

1. 执行完毕后，可以通过浏览器访问远程机器
