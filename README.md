
### 安装库
```
pip install -r requirements.txt
pip install -U python-dotenv
```


### 数据库表

```
CREATE TABLE `address` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(16) NOT NULL DEFAULT '',
  `mobile` varchar(16) NOT NULL DEFAULT '',
  `address` varchar(128) NOT NULL,
  `created_at` int(10) unsigned NOT NULL DEFAULT '0',
  `updated_at` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8 COMMENT='绑定地址表';


CREATE TABLE `member` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(20) NOT NULL DEFAULT '' COMMENT '姓名',
  `wx_code` varchar(24) NOT NULL DEFAULT '',
  `is_member` varchar(2) NOT NULL COMMENT '是否会员',
  `warranty_time` varchar(20) NOT NULL COMMENT '保修期',
  `wx_name` varchar(50) NOT NULL COMMENT '微信号',
  `member_grade` varchar(20) NOT NULL COMMENT '会员等级',
  `created_at` int(20) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `updated_at` int(20) unsigned NOT NULL DEFAULT '0' COMMENT '修改时间',
  `mobile` varchar(20) NOT NULL COMMENT '电话',
  `address` varchar(500) NOT NULL COMMENT '地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;



CREATE TABLE `member_types` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `member_price` varchar(20) NOT NULL COMMENT '价格',
  `member_title` varchar(50) NOT NULL COMMENT '会员标题',
  `member_describe` varchar(100) NOT NULL DEFAULT '' COMMENT '会员描述',
  `member_limit` varchar(100) NOT NULL DEFAULT '' COMMENT '会员限制',
  `member_details` varchar(1000) NOT NULL DEFAULT '' COMMENT '会员详情',
  `number` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '使用次数',
  `created_at` int(20) unsigned NOT NULL DEFAULT '0',
  `updated_at` int(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;


CREATE TABLE `repair_order` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `sn` varchar(20) NOT NULL,
  `transaction_id` varchar(32) NOT NULL DEFAULT '' COMMENT '微信订单号',
  `mobile` varchar(20) NOT NULL COMMENT '电话',
  `name` varchar(20) NOT NULL COMMENT '姓名',
  `pay_type` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '支付状态 1 已支付，0 未支付, 2 未付完',
  `type` varchar(50) NOT NULL DEFAULT '',
  `status` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '0进行中\\n1已结束',
  `category_name` varchar(50) NOT NULL DEFAULT '' COMMENT '清洁分类',
  `price` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '价格',
  `pay_price` decimal(10,2) NOT NULL DEFAULT '0.00',
  `time_end` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '支付结束时间',
  `city_code` varchar(8) NOT NULL COMMENT '市',
  `address` varchar(50) NOT NULL COMMENT '住址',
  `province_code` varchar(20) NOT NULL COMMENT '省',
  `created_at` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `updated_at` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '修改时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8 COMMENT='订单表';


CREATE TABLE `types` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `type_name` varchar(20) NOT NULL COMMENT '类别名称',
  `type_type` varchar(20) NOT NULL DEFAULT '' COMMENT '类别分类',
  `created_at` int(15) unsigned NOT NULL DEFAULT '0' COMMENT '创建时间',
  `updated_at` int(15) unsigned NOT NULL DEFAULT '0' COMMENT '修改时间',
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;


CREATE TABLE `types_category` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '编号',
  `category_name` varchar(20) NOT NULL DEFAULT '' COMMENT '分类名称',
  `price` int(11) NOT NULL DEFAULT '0' COMMENT '价格',
  `type_id` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '类别编码',
  `created_at` int(11) unsigned NOT NULL DEFAULT '0',
  `updated_at` int(11) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
```

### 开发环境 访问地址
http://www.a.com/admin/login 登录地址

### 开发环境 api地址

### 配置项目需要在根目录定义.env 请参考.env.dist