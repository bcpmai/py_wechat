### 开发环境 访问地址
http://www.a.com/admin/login 登录地址

### 开发环境 api地址


### 数据库表

--
-- 表的结构 `address`
--

CREATE TABLE `address` (
  `id` int(10) UNSIGNED NOT NULL,
  `username` varchar(16) NOT NULL DEFAULT '',
  `mobile` varchar(16) NOT NULL DEFAULT '',
  `address` varchar(128) NOT NULL,
  `created_at` int(10) NOT NULL DEFAULT '0',
  `updated_at` int(10) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='绑定地址表';

-- --------------------------------------------------------

--
-- 表的结构 `member`
--

CREATE TABLE `member` (
  `id` int(10) NOT NULL,
  `user_name` varchar(20) NOT NULL COMMENT '姓名',
  `wx_code` varchar(24) DEFAULT NULL,
  `is_member` varchar(2) NOT NULL COMMENT '是否会员',
  `warranty_time` varchar(20) NOT NULL COMMENT '保修期',
  `wx_name` varchar(50) NOT NULL COMMENT '微信号',
  `member_grade` varchar(20) NOT NULL COMMENT '会员等级',
  `created_at` int(20) NOT NULL COMMENT '创建时间',
  `updated_at` int(20) NOT NULL COMMENT '修改时间',
  `mobile` varchar(20) NOT NULL COMMENT '电话',
  `address` varchar(500) NOT NULL COMMENT '地址'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `membertypes`
--

CREATE TABLE `membertypes` (
  `id` int(10) NOT NULL,
  `member_price` varchar(20) NOT NULL COMMENT '价格',
  `member_title` varchar(50) NOT NULL COMMENT '会员标题',
  `member_describe` varchar(100) DEFAULT NULL COMMENT '会员描述',
  `member_limit` varchar(100) DEFAULT NULL COMMENT '会员限制',
  `member_details` varchar(1000) DEFAULT NULL COMMENT '会员详情',
  `created_at` int(20) NOT NULL,
  `updated_at` int(20) NOT NULL,
  `number` int(11) DEFAULT '1' COMMENT '使用次数'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `repair_order`
--

CREATE TABLE `repair_order` (
  `id` int(10) NOT NULL,
  `sn` varchar(20) NOT NULL,
  `transaction_id` varchar(32) NOT NULL DEFAULT '' COMMENT '微信订单号',
  `mobile` varchar(20) NOT NULL COMMENT '电话',
  `name` varchar(20) NOT NULL COMMENT '姓名',
  `pay_type` int(11) NOT NULL DEFAULT '0' COMMENT '支付状态 1 已支付，0 未支付, 2 未付完',
  `created_at` int(10) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `updated_at` int(10) NOT NULL DEFAULT '0' COMMENT '修改时间',
  `type` varchar(50) NOT NULL DEFAULT '',
  `status` int(11) DEFAULT '0' COMMENT '0进行中\n1已结束',
  `category_name` varchar(50) NOT NULL DEFAULT '' COMMENT '清洁分类',
  `price` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '价格',
  `pay_price` decimal(10,2) DEFAULT '0.00',
  `time_end` int(11) DEFAULT '0' COMMENT '支付结束时间',
  `city_code` varchar(8) NOT NULL COMMENT '市',
  `address` varchar(50) NOT NULL COMMENT '住址',
  `province_code` varchar(20) NOT NULL COMMENT '省'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='订单表';

-- --------------------------------------------------------

--
-- 表的结构 `types`
--

CREATE TABLE `types` (
  `id` int(10) NOT NULL,
  `type_name` varchar(20) NOT NULL COMMENT '类别名称',
  `created_at` int(15) NOT NULL COMMENT '创建时间',
  `updated_at` int(15) NOT NULL COMMENT '修改时间',
  `type_type` varchar(20) DEFAULT NULL COMMENT '类别分类'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `types_category`
--

CREATE TABLE `types_category` (
  `category_name` varchar(20) DEFAULT NULL COMMENT '分类名称',
  `id` int(11) NOT NULL COMMENT '编号',
  `price` int(11) DEFAULT NULL COMMENT '价格',
  `type_id` int(11) NOT NULL COMMENT '类别编码',
  `created_at` int(11) DEFAULT '20',
  `updated_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `member_id_uindex` (`id`);

--
-- Indexes for table `membertypes`
--
ALTER TABLE `membertypes`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `repair_order`
--
ALTER TABLE `repair_order`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `repair_order_id_uindex` (`id`);

--
-- Indexes for table `types`
--
ALTER TABLE `types`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `types_category`
--
ALTER TABLE `types_category`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `address`
--
ALTER TABLE `address`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- 使用表AUTO_INCREMENT `member`
--
ALTER TABLE `member`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- 使用表AUTO_INCREMENT `membertypes`
--
ALTER TABLE `membertypes`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- 使用表AUTO_INCREMENT `repair_order`
--
ALTER TABLE `repair_order`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;
--
-- 使用表AUTO_INCREMENT `types`
--
ALTER TABLE `types`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- 使用表AUTO_INCREMENT `types_category`
--
ALTER TABLE `types_category`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '编号', AUTO_INCREMENT=11;