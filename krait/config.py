#!/usr/bin/env python
# -*- coding:utf-8 -*-
import logging as log
import argparse
import json
import toml

# 配置命令行参数的例子
"""
# 应用程序名
"application" = "falcon::toolkit"

# 应用级参数列表
"application_args" = [
	{
		"name"	   = "-c, --app-config", 
		"help" 	   = "application configuration",
		"required" = true
	},
	{
		"name"	   = "-l, --log-config",
		"help" 	   = "logger configuration",
		"required" = true
	},
	{
		"name"	   = "-d",
		"help" 	   = "desc application",
		"required" = false
	}
]

# 子应用列表
"sub_module" = ["crawl", "parser"]

# 每个子应用的参数列表
"crawl" = [
	{
		"name"	   = "-o, --output-dir", 
		"help" 	   = "output dir",
		"required" = true
	},
	{
		"name"	   = "-i, --input-dir", 
		"help" 	   = "input dir",
		"required" = true
	}
]

"parser" = [
	{
		"name"	   = "-i, --input-dir", 
		"help" 	   = "input dir",
		"required" = true
	}
]
"""

#
# 根据配置文件解析命令行参数
def args_parse(args_info: str) -> argparse.Namespace:
	D = toml.loads(args_info)
	# print(D)
	parser = argparse.ArgumentParser(prog=D['application'])
	# 首先解析应用程序级别的参数
	for c in D['application_args']:
		d = {}
		d['help'] = c['help']
		if c['required'] == True:
			d['help'] = "[*required] " + c['help']
		d['required'] = c['required']
		d['metavar'] = ""
		parser.add_argument(*c['name'].split(' '), **d)
	# 如果没有子模块，直接返回
	if 'sub_module' not in D:
		return parser.parse_args()
	# 处理子模块命令行参数
	subparsers = parser.add_subparsers(help='sub module help', dest="module")
	for m in D['sub_module']:
		parser_tagger = subparsers.add_parser(m, help='{} help information'.format(m))
		for c in D[m]:
			d = {}
			d['help'] = c['help']
			if c['required'] == True:
				d['help'] = "[*required] " + c['help']
			d['required'] = c['required']
			d['metavar'] = ""
			parser_tagger.add_argument(*c['name'].split(' '), **d)
	# 解析参数
	return parser.parse_args()

#
# 根据配置文件配置日志模块
#  - config_filename : 日志信息配置文件
#  - section		 : 配置项 
def setup_logger(app: str, module: str, config_filename: str="") -> None:
	# 定义日志级别对应关系表
	level_relations = {
		'debug'  : log.DEBUG,
		'info'   : log.INFO,
		'warning': log.WARNING,
		'error'  : log.ERROR,
		'crit'   : log.CRITICAL
	}
	# 如果没有指定配置文件
	if config_filename == "":
		log.basicConfig(format="[%(asctime)s][%(levelname)s] %(message)s", level=log.DEBUG, datefmt='%m/%d %I:%M:%S')
		return 
	# 加载配置文件
	C = ""
	with open(config_filename, "r") as config_file:
		C = json.load(config_file)
	# 日志输出格式
	fmt = "[%(asctime)s][%(levelname)s] %(message)s"
	# 日志输出级别
	log_level = level_relations[C['level']]
	# 日志输出到文件
	if 'filename' in C:
		mode = 'w'
		if 'filemode' in C:
			mode = C['filemode']
		if 'format' in C:
			fmt = C['format']
		log.basicConfig(filename=C['filename'].format(app=app, module=module), filemode=mode, format=fmt, level=log_level)
		# 是否同时输出到屏幕
		if "console" in C:
			console = log.StreamHandler()
			console.setLevel(level_relations[C['console']])
			console.setFormatter(log.Formatter(fmt))
			log.getLogger('').addHandler(console)

#
# 读取JSON配置文件
def load_json(fname: str) -> dict:
	C = {}
	with open(fname, "r") as f:
		C = json.load(f)
	return C



