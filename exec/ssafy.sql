-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: mysql
-- 생성 시간: 24-11-19 01:11
-- 서버 버전: 8.0.40
-- PHP 버전: 8.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `ssafy`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `approve_request`
--

CREATE TABLE `approve_request` (
  `approve_request_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `family_id` bigint NOT NULL,
  `family_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `family_phone_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senior_birth` datetime(6) NOT NULL,
  `senior_id` bigint NOT NULL,
  `senior_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senior_phone_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` enum('APPROVED','PENDING','REJECTED') COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `member_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `conversation`
--

CREATE TABLE `conversation` (
  `conversation_id` bigint NOT NULL,
  `senior_id` bigint DEFAULT '1',
  `start_date` date NOT NULL,
  `end_time` time DEFAULT NULL,
  `memory_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `avg_score` float DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `conversation`
--

INSERT INTO `conversation` (`conversation_id`, `senior_id`, `start_date`, `end_time`, `memory_id`, `avg_score`) VALUES
(80, 1, '2024-11-17', '17:31:42', '9db7ffdb-64bd-4a04-ad73-b40a611ba142', 86),
(88, 1, '2024-11-13', '12:15:30', 'mem008', 63),
(89, 1, '2024-11-13', '20:00:45', 'mem009', 72),
(91, 1, '2024-11-14', '15:30:20', 'mem011', 68),
(92, 1, '2024-11-14', '18:45:50', 'mem012', 68),
(93, 1, '2024-11-15', '07:40:30', 'mem013', 13),
(94, 1, '2024-11-15', '14:10:00', 'mem014', 35),
(96, 1, '2024-11-16', '10:30:45', 'mem016', 45),
(98, 1, '2024-11-16', '22:20:30', 'mem018', 45),
(99, 1, '2024-11-17', '09:00:00', 'mem019', 86),
(100, 1, '2024-11-17', '13:30:25', 'mem020', 86),
(112, 1, '2024-11-18', '15:33:58', 'b8807089-b18b-464c-9d2b-d607ca68df10', 55),
(117, 1, '2024-11-18', '16:35:14', '3941cc15-25e1-4961-98a4-5044b1b3ccb9', 57.5),
(119, 1, '2024-11-18', '17:03:48', 'c5452d22-1343-4b88-a941-77446af59631', 53),
(122, 1, '2024-11-19', '07:40:45', 'c5452d22-1343-4b88-a941-77446af59613', 37),
(123, 1, '2024-11-19', '09:53:52', '26683a23-f60d-4063-98a8-f243cd5c76b6', 40);

-- --------------------------------------------------------

--
-- 테이블 구조 `ENTRY_HISTORY`
--

CREATE TABLE `ENTRY_HISTORY` (
  `DURATION_TIME` bigint NOT NULL,
  `ENTRY_HISTORY_ID` bigint NOT NULL,
  `SENIOR_ID` bigint DEFAULT NULL,
  `PLACE` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `entry_history`
--

CREATE TABLE `entry_history` (
  `entry_history_id` bigint NOT NULL,
  `duration_time` bigint NOT NULL,
  `place` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senior_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `EXIT_HISTORY`
--

CREATE TABLE `EXIT_HISTORY` (
  `EXIT_AT` timestamp(6) NOT NULL,
  `EXIT_HISTORY_ID` bigint NOT NULL,
  `SENIOR_ID` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `exit_history`
--

CREATE TABLE `exit_history` (
  `exit_history_id` bigint NOT NULL,
  `exit_at` datetime(6) NOT NULL,
  `senior_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `MEMBER`
--

CREATE TABLE `MEMBER` (
  `CREATED_AT` timestamp(6) NOT NULL,
  `MEMBER_ID` bigint NOT NULL,
  `UPDATED_AT` timestamp(6) NOT NULL,
  `LOGIN_ID` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PASSWORD` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PHONE_NUMBER` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `TYPE` enum('FAMILY','SOCIAL_WORKER') COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `member`
--

CREATE TABLE `member` (
  `member_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `login_id` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `type` enum('FAMILY','SOCIAL_WORKER') COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `member`
--

INSERT INTO `member` (`member_id`, `created_at`, `login_id`, `name`, `password`, `phone_number`, `type`, `updated_at`) VALUES
(1, '2024-11-14 01:23:58.285971', 'ssafytest', '윤정섭', '$2a$10$9DqYvrK5RT49ezqP9eHrGeccj0tDAeuZxlxCZHLIkoCEl7RMyZWoC', '010-4389-6501', 'SOCIAL_WORKER', '2024-11-14 01:23:58.286038'),
(2, '2024-11-14 01:28:14.949897', 'ssafytest2', '유병주', '$2a$10$4Dm6Ol6rdW342A0xJ.A/k.vFEeRaSD3vU/bWZNVH4riioU1UqABNq', '010-7731-2893', 'FAMILY', '2024-11-14 01:28:14.949931');

-- --------------------------------------------------------

--
-- 테이블 구조 `member_fcm_token`
--

CREATE TABLE `member_fcm_token` (
  `member_fcm_token_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `fcm_token` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `member_id` bigint NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `member_fcm_token`
--

INSERT INTO `member_fcm_token` (`member_fcm_token_id`, `created_at`, `fcm_token`, `updated_at`, `member_id`) VALUES
(22, '2024-11-19 00:20:12.763790', 'f1nEqiiVQpGegxnEbWfZyK:APA91bFavfi0S32RX_qOEVvFbhCJLZs8jgmb5J9AlGvUmUGZAs6Ta8af1Xua9EzUgALehBQbGH5_YPOeXzywVGV67OJg16VY_ox9TOuF3U4vxCl-FOY1zKk', '2024-11-19 00:41:18.396727', 1),
(23, '2024-11-19 00:41:57.485194', 'ftdWdND9So-_liU4ukZxXg:APA91bEGBzvxaoT67xsn-vM8tGXaf2vb6f8z0ZRXbGn7fidd_mMhShYXE_aP9e2AXcpcOY5tLnm16iJhW87EhmAsG8DAJ9ZLgIaW8KKcBRiNVLIzeCsju-4', '2024-11-19 00:41:57.485214', 2);

-- --------------------------------------------------------

--
-- 테이블 구조 `MEMBER_SENIOR`
--

CREATE TABLE `MEMBER_SENIOR` (
  `MEMBER_ID` bigint DEFAULT NULL,
  `MEMBER_SENIOR_ID` bigint NOT NULL,
  `SENIOR_ID` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `member_senior`
--

CREATE TABLE `member_senior` (
  `member_senior_id` bigint NOT NULL,
  `is_social_worker` bit(1) DEFAULT NULL,
  `member_id` bigint DEFAULT NULL,
  `senior_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `member_senior`
--

INSERT INTO `member_senior` (`member_senior_id`, `is_social_worker`, `member_id`, `senior_id`) VALUES
(1, b'1', 1, 1),
(2, b'1', 1, 2),
(3, b'1', 1, 3),
(4, b'1', 1, 4);

-- --------------------------------------------------------

--
-- 테이블 구조 `memory`
--

CREATE TABLE `memory` (
  `id` int NOT NULL,
  `memory_id` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `conversation_id` bigint DEFAULT NULL,
  `speaker` enum('AI','User') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `content` text COLLATE utf8mb4_unicode_ci,
  `summary` text COLLATE utf8mb4_unicode_ci,
  `positivity_score` int DEFAULT '50',
  `keywords` json DEFAULT NULL,
  `response_plan` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `memory`
--

INSERT INTO `memory` (`id`, `memory_id`, `conversation_id`, `speaker`, `content`, `summary`, `positivity_score`, `keywords`, `response_plan`) VALUES
(311, '26683a23-f60d-4063-98a8-f243cd5c76b6', 123, 'AI', '네! 부르셨나요?', NULL, 50, '[]', '[]'),
(312, '26683a23-f60d-4063-98a8-f243cd5c76b6', 123, 'User', '1990년 당국 노래 알려줘', NULL, 50, '[]', '[]'),
(313, '26683a23-f60d-4063-98a8-f243cd5c76b6', 123, 'AI', '1990년대의 음악은 정말 많은 사람들에게 특별한 기억을 남겼죠. 특히 그 시기에 유행했던 노래들은 많은 이들에게 감정을 불러일으키곤 했습니다. 어떤 특정한 노래를 말씀하고 싶으신 건가요? 그 노래와 관련된 기억이 있으신지 궁금합니다.', '1990년대의 당국 노래에 대한 요청으로, 노래에 대한 긍정적인 관심을 나타냄.', 65, '[\"1990년\", \"당국\", \"노래\"]', '[]'),
(314, '26683a23-f60d-4063-98a8-f243cd5c76b6', 123, 'User', '항공 노래 알려주면 될 거 같애', NULL, 50, '[]', '[]'),
(315, '26683a23-f60d-4063-98a8-f243cd5c76b6', 123, 'AI', '항공에 관한 노래를 찾고 계시는군요. 그런 노래는 여행의 설렘이나 하늘을 나는 기분을 잘 담고 있죠. 어떤 특정한 주제나 감정이 담긴 노래를 원하시는지 궁금해요. 예를 들어, 여행의 즐거움, 그리움, 혹은 기분 좋은 순간 같은 것이요. 어떤 노래를 찾고 계신가요?', '항공과 관련된 노래를 알려달라는 요청입니다.', 75, '[\"항공\", \"노래\", \"알려주다\"]', '[]');

-- --------------------------------------------------------

--
-- 테이블 구조 `QUALIFY_NUM`
--

CREATE TABLE `QUALIFY_NUM` (
  `QUALIFY_NUM_ID` bigint NOT NULL,
  `QUALIFY_NUMBER` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `qualify_num`
--

CREATE TABLE `qualify_num` (
  `qualify_num_id` bigint NOT NULL,
  `in_use` bit(1) NOT NULL DEFAULT b'0',
  `qualify_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `qualify_num`
--

INSERT INTO `qualify_num` (`qualify_num_id`, `in_use`, `qualify_number`) VALUES
(1, b'1', 'volunteer00001'),
(2, b'0', 'volunteer_0001');

-- --------------------------------------------------------

--
-- 테이블 구조 `SCHEDULE`
--

CREATE TABLE `SCHEDULE` (
  `CREATE_AT` timestamp(6) NOT NULL,
  `SCHEDULE_AT` timestamp(6) NOT NULL,
  `SCHEDULE_ID` bigint NOT NULL,
  `SENIOR_ID` bigint DEFAULT NULL,
  `MEMO` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `schedule`
--

CREATE TABLE `schedule` (
  `schedule_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `memo` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_at` datetime DEFAULT NULL,
  `senior_id` bigint DEFAULT NULL,
  `end_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `schedule`
--

INSERT INTO `schedule` (`schedule_id`, `created_at`, `memo`, `start_at`, `senior_id`, `end_at`) VALUES
(1, '2024-11-15 09:00:00.000000', '치과 진료', '2024-11-11 09:00:00', 1, '2024-11-11 10:30:00'),
(2, '2024-11-15 09:00:00.000000', '외과', '2024-11-27 14:00:00', 1, '2024-11-27 15:30:00'),
(3, '2024-11-15 09:00:00.000000', '정형외과', '2024-11-16 11:00:00', 1, '2024-11-16 12:30:00'),
(4, '2024-11-15 09:00:00.000000', '치과 방문', '2024-11-19 13:30:00', 1, '2024-11-19 14:00:00'),
(5, '2024-11-15 09:00:00.000000', '가스 점검 방문', '2024-11-19 16:10:00', 1, '2024-11-19 17:00:00'),
(9, '2024-11-16 14:01:58.146048', '명상의 시간', '2024-11-10 21:00:00', 1, '2024-11-10 22:00:00'),
(10, '2024-11-16 18:14:48.275147', '명상 수업', '2024-11-08 13:00:00', 1, '2024-11-08 17:00:00'),
(14, '2024-10-01 09:30:00.000000', '치과 방문', '2024-10-04 09:00:00', 1, '2024-10-04 10:00:00'),
(15, '2024-10-01 09:30:00.000000', '산책', '2024-10-07 10:30:00', 1, '2024-10-07 12:00:00'),
(16, '2024-10-01 09:30:00.000000', '약국 방문', '2024-10-10 11:00:00', 1, '2024-10-10 11:30:00'),
(17, '2024-10-01 09:30:00.000000', '마트 장보기', '2024-10-13 13:00:00', 1, '2024-10-13 14:30:00'),
(18, '2024-10-01 09:30:00.000000', '가족 모임', '2024-10-23 15:00:00', 1, '2024-10-23 17:00:00'),
(19, '2024-10-01 09:30:00.000000', '병원 진료', '2024-10-27 10:00:00', 1, '2024-10-27 11:30:00'),
(20, '2024-10-01 09:30:00.000000', '병원 진료', '2024-12-01 09:00:00', 1, '2024-12-01 10:30:00'),
(21, '2024-10-01 09:30:00.000000', '동네 모임', '2024-12-05 10:30:00', 1, '2024-12-05 12:00:00'),
(22, '2024-10-01 09:30:00.000000', '가스 점검', '2024-12-14 14:00:00', 1, '2024-12-14 15:30:00'),
(23, '2024-10-01 09:30:00.000000', '병원 진료', '2024-12-21 09:00:00', 1, '2024-12-21 10:00:00'),
(24, '2024-10-01 09:30:00.000000', '친구 모임', '2024-12-24 13:00:00', 1, '2024-12-24 15:00:00');

-- --------------------------------------------------------

--
-- 테이블 구조 `SENIOR`
--

CREATE TABLE `SENIOR` (
  `BIRTH` timestamp(6) NOT NULL,
  `CREATED_AT` timestamp(6) NOT NULL,
  `SENIOR_ID` bigint NOT NULL,
  `UPDATED_AT` timestamp(6) NOT NULL,
  `ADDRESS` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `NAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PHONE_NUMBER` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `PROFILE_IMG` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `GENDER` enum('FEMALE','MALE') COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `senior`
--

CREATE TABLE `senior` (
  `senior_id` bigint NOT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `birth` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `gender` enum('FEMALE','MALE') COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone_number` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profile_img` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `senior`
--

INSERT INTO `senior` (`senior_id`, `address`, `birth`, `created_at`, `gender`, `name`, `phone_number`, `profile_img`, `updated_at`) VALUES
(1, '인천광역시 서구', '1939-04-05 00:00:00.000000', '2024-11-14 01:34:40.136115', 'MALE', '이강현', '010-1234-5678', 'https://jungkkiri.s3.ap-northeast-2.amazonaws.com/senior_profile_img/1/fdc205b2-9c39-47c3-8fd5-aabdc506da8aabc.jpg', '2024-11-18 23:49:53.354700'),
(2, '서울특별시 강남구', '1928-07-07 00:00:00.000000', '2024-11-14 01:34:40.139132', 'FEMALE', '박정의', '010-2580-1357', 'https://jungkkiri.s3.ap-northeast-2.amazonaws.com/senior_profile_img/2/d9fbcbd0-d111-4e6b-b5a8-76409b3a3e09profile.jpg', '2024-11-18 17:04:54.883035'),
(3, '서울특별시 송파구', '1942-11-01 00:00:00.000000', '2024-11-14 01:34:40.142200', 'MALE', '임동길', '010-8765-4321', 'https://jungkkiri.s3.ap-northeast-2.amazonaws.com/senior_profile_img/0/07610884-fe0c-4943-9bc7-0f12a7cbc256%EC%BA%A1%EC%B2%98.PNG', '2024-11-14 01:34:40.142226'),
(4, '경기도 고양시', '1919-02-24 09:00:00.000000', '2024-11-14 01:34:40.144952', 'MALE', '안홍찬', '010-1357-2468', 'https://jungkkiri.s3.ap-northeast-2.amazonaws.com/senior_profile_img/0/07610884-fe0c-4943-9bc7-0f12a7cbc256%EC%BA%A1%EC%B2%98.PNG', '2024-11-18 14:03:12.254043');

-- --------------------------------------------------------

--
-- 테이블 구조 `speaker`
--

CREATE TABLE `speaker` (
  `speaker_id` bigint NOT NULL,
  `serial_num` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `senior_id` bigint DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- 테이블 구조 `TEAM`
--

CREATE TABLE `TEAM` (
  `TEAM_ID` bigint NOT NULL,
  `NAME` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- 테이블의 덤프 데이터 `TEAM`
--

INSERT INTO `TEAM` (`TEAM_ID`, `NAME`) VALUES
(1, 'test1');

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `approve_request`
--
ALTER TABLE `approve_request`
  ADD PRIMARY KEY (`approve_request_id`),
  ADD KEY `FKo9t0jeqvabf4s4c7a5qymuq7v` (`member_id`);

--
-- 테이블의 인덱스 `conversation`
--
ALTER TABLE `conversation`
  ADD PRIMARY KEY (`conversation_id`),
  ADD KEY `FK5mpj5asmgi59lp6wqf7mm274f` (`senior_id`);

--
-- 테이블의 인덱스 `ENTRY_HISTORY`
--
ALTER TABLE `ENTRY_HISTORY`
  ADD PRIMARY KEY (`ENTRY_HISTORY_ID`),
  ADD KEY `FK_ENTRY_HISTORY_SENIOR` (`SENIOR_ID`);

--
-- 테이블의 인덱스 `entry_history`
--
ALTER TABLE `entry_history`
  ADD PRIMARY KEY (`entry_history_id`),
  ADD KEY `FK5sk0entcfq0w5hjigv50cqmu6` (`senior_id`);

--
-- 테이블의 인덱스 `EXIT_HISTORY`
--
ALTER TABLE `EXIT_HISTORY`
  ADD PRIMARY KEY (`EXIT_HISTORY_ID`),
  ADD KEY `FK_EXIT_HISTORY_SENIOR` (`SENIOR_ID`);

--
-- 테이블의 인덱스 `exit_history`
--
ALTER TABLE `exit_history`
  ADD PRIMARY KEY (`exit_history_id`),
  ADD KEY `FKo9f7wvtty61yo9xxx1ktb4i84` (`senior_id`);

--
-- 테이블의 인덱스 `MEMBER`
--
ALTER TABLE `MEMBER`
  ADD PRIMARY KEY (`MEMBER_ID`),
  ADD UNIQUE KEY `LOGIN_ID` (`LOGIN_ID`);

--
-- 테이블의 인덱스 `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`member_id`),
  ADD UNIQUE KEY `UKenfm5patwjqulw8k4wwuo6f60` (`login_id`);

--
-- 테이블의 인덱스 `member_fcm_token`
--
ALTER TABLE `member_fcm_token`
  ADD PRIMARY KEY (`member_fcm_token_id`),
  ADD KEY `FK1t32tfi2x0x2xl8te76jm3q2u` (`member_id`);

--
-- 테이블의 인덱스 `MEMBER_SENIOR`
--
ALTER TABLE `MEMBER_SENIOR`
  ADD PRIMARY KEY (`MEMBER_SENIOR_ID`),
  ADD KEY `FK_MEMBER_SENIOR_SENIOR` (`SENIOR_ID`),
  ADD KEY `FK_MEMBER_SENIOR_MEMBER` (`MEMBER_ID`);

--
-- 테이블의 인덱스 `member_senior`
--
ALTER TABLE `member_senior`
  ADD PRIMARY KEY (`member_senior_id`),
  ADD KEY `FKs2aqlnk76jpkg4u7hfy9p8380` (`member_id`),
  ADD KEY `FKfefxlklm5rvm0f7rtbjpmbfy2` (`senior_id`);

--
-- 테이블의 인덱스 `memory`
--
ALTER TABLE `memory`
  ADD PRIMARY KEY (`id`),
  ADD KEY `conversation_id` (`conversation_id`);

--
-- 테이블의 인덱스 `QUALIFY_NUM`
--
ALTER TABLE `QUALIFY_NUM`
  ADD PRIMARY KEY (`QUALIFY_NUM_ID`),
  ADD UNIQUE KEY `QUALIFY_NUMBER` (`QUALIFY_NUMBER`);

--
-- 테이블의 인덱스 `qualify_num`
--
ALTER TABLE `qualify_num`
  ADD PRIMARY KEY (`qualify_num_id`),
  ADD UNIQUE KEY `UKmyo4uu7j05eww4roav7gfpndq` (`qualify_number`);

--
-- 테이블의 인덱스 `SCHEDULE`
--
ALTER TABLE `SCHEDULE`
  ADD PRIMARY KEY (`SCHEDULE_ID`),
  ADD KEY `FK_SCHEDULE_SENIOR` (`SENIOR_ID`);

--
-- 테이블의 인덱스 `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`schedule_id`),
  ADD KEY `FKp5x0msimvyjoc19bcwtvwbeoy` (`senior_id`);

--
-- 테이블의 인덱스 `SENIOR`
--
ALTER TABLE `SENIOR`
  ADD PRIMARY KEY (`SENIOR_ID`);

--
-- 테이블의 인덱스 `senior`
--
ALTER TABLE `senior`
  ADD PRIMARY KEY (`senior_id`),
  ADD UNIQUE KEY `UK50lyk7vs7u7i8n07lk6wuuwel` (`phone_number`);

--
-- 테이블의 인덱스 `speaker`
--
ALTER TABLE `speaker`
  ADD PRIMARY KEY (`speaker_id`),
  ADD UNIQUE KEY `UKtjmn88mcb0asx3mleq0ivnktq` (`serial_num`),
  ADD UNIQUE KEY `UKdsjalqm2jqp8qgx5xhdbsoesl` (`senior_id`);

--
-- 테이블의 인덱스 `TEAM`
--
ALTER TABLE `TEAM`
  ADD PRIMARY KEY (`TEAM_ID`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `approve_request`
--
ALTER TABLE `approve_request`
  MODIFY `approve_request_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- 테이블의 AUTO_INCREMENT `conversation`
--
ALTER TABLE `conversation`
  MODIFY `conversation_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=124;

--
-- 테이블의 AUTO_INCREMENT `ENTRY_HISTORY`
--
ALTER TABLE `ENTRY_HISTORY`
  MODIFY `ENTRY_HISTORY_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `entry_history`
--
ALTER TABLE `entry_history`
  MODIFY `entry_history_id` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `EXIT_HISTORY`
--
ALTER TABLE `EXIT_HISTORY`
  MODIFY `EXIT_HISTORY_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `exit_history`
--
ALTER TABLE `exit_history`
  MODIFY `exit_history_id` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `MEMBER`
--
ALTER TABLE `MEMBER`
  MODIFY `MEMBER_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `member`
--
ALTER TABLE `member`
  MODIFY `member_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 테이블의 AUTO_INCREMENT `member_fcm_token`
--
ALTER TABLE `member_fcm_token`
  MODIFY `member_fcm_token_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- 테이블의 AUTO_INCREMENT `MEMBER_SENIOR`
--
ALTER TABLE `MEMBER_SENIOR`
  MODIFY `MEMBER_SENIOR_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `member_senior`
--
ALTER TABLE `member_senior`
  MODIFY `member_senior_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- 테이블의 AUTO_INCREMENT `memory`
--
ALTER TABLE `memory`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=316;

--
-- 테이블의 AUTO_INCREMENT `QUALIFY_NUM`
--
ALTER TABLE `QUALIFY_NUM`
  MODIFY `QUALIFY_NUM_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `qualify_num`
--
ALTER TABLE `qualify_num`
  MODIFY `qualify_num_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 테이블의 AUTO_INCREMENT `SCHEDULE`
--
ALTER TABLE `SCHEDULE`
  MODIFY `SCHEDULE_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `schedule`
--
ALTER TABLE `schedule`
  MODIFY `schedule_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- 테이블의 AUTO_INCREMENT `SENIOR`
--
ALTER TABLE `SENIOR`
  MODIFY `SENIOR_ID` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `senior`
--
ALTER TABLE `senior`
  MODIFY `senior_id` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- 테이블의 AUTO_INCREMENT `speaker`
--
ALTER TABLE `speaker`
  MODIFY `speaker_id` bigint NOT NULL AUTO_INCREMENT;

--
-- 테이블의 AUTO_INCREMENT `TEAM`
--
ALTER TABLE `TEAM`
  MODIFY `TEAM_ID` bigint NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 덤프된 테이블의 제약사항
--

--
-- 테이블의 제약사항 `approve_request`
--
ALTER TABLE `approve_request`
  ADD CONSTRAINT `FKo9t0jeqvabf4s4c7a5qymuq7v` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`);

--
-- 테이블의 제약사항 `conversation`
--
ALTER TABLE `conversation`
  ADD CONSTRAINT `FK5mpj5asmgi59lp6wqf7mm274f` FOREIGN KEY (`senior_id`) REFERENCES `senior` (`senior_id`);

--
-- 테이블의 제약사항 `ENTRY_HISTORY`
--
ALTER TABLE `ENTRY_HISTORY`
  ADD CONSTRAINT `FK_ENTRY_HISTORY_SENIOR` FOREIGN KEY (`SENIOR_ID`) REFERENCES `SENIOR` (`SENIOR_ID`);

--
-- 테이블의 제약사항 `entry_history`
--
ALTER TABLE `entry_history`
  ADD CONSTRAINT `FK5sk0entcfq0w5hjigv50cqmu6` FOREIGN KEY (`senior_id`) REFERENCES `senior` (`senior_id`);

--
-- 테이블의 제약사항 `EXIT_HISTORY`
--
ALTER TABLE `EXIT_HISTORY`
  ADD CONSTRAINT `FK_EXIT_HISTORY_SENIOR` FOREIGN KEY (`SENIOR_ID`) REFERENCES `SENIOR` (`SENIOR_ID`);

--
-- 테이블의 제약사항 `exit_history`
--
ALTER TABLE `exit_history`
  ADD CONSTRAINT `FKo9f7wvtty61yo9xxx1ktb4i84` FOREIGN KEY (`senior_id`) REFERENCES `senior` (`senior_id`);

--
-- 테이블의 제약사항 `member_fcm_token`
--
ALTER TABLE `member_fcm_token`
  ADD CONSTRAINT `FK1t32tfi2x0x2xl8te76jm3q2u` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`);

--
-- 테이블의 제약사항 `MEMBER_SENIOR`
--
ALTER TABLE `MEMBER_SENIOR`
  ADD CONSTRAINT `FK_MEMBER_SENIOR_MEMBER` FOREIGN KEY (`MEMBER_ID`) REFERENCES `MEMBER` (`MEMBER_ID`),
  ADD CONSTRAINT `FK_MEMBER_SENIOR_SENIOR` FOREIGN KEY (`SENIOR_ID`) REFERENCES `SENIOR` (`SENIOR_ID`);

--
-- 테이블의 제약사항 `member_senior`
--
ALTER TABLE `member_senior`
  ADD CONSTRAINT `FKfefxlklm5rvm0f7rtbjpmbfy2` FOREIGN KEY (`senior_id`) REFERENCES `senior` (`senior_id`),
  ADD CONSTRAINT `FKs2aqlnk76jpkg4u7hfy9p8380` FOREIGN KEY (`member_id`) REFERENCES `member` (`member_id`);

--
-- 테이블의 제약사항 `memory`
--
ALTER TABLE `memory`
  ADD CONSTRAINT `memory_ibfk_1` FOREIGN KEY (`conversation_id`) REFERENCES `conversation` (`conversation_id`);

--
-- 테이블의 제약사항 `SCHEDULE`
--
ALTER TABLE `SCHEDULE`
  ADD CONSTRAINT `FK_SCHEDULE_SENIOR` FOREIGN KEY (`SENIOR_ID`) REFERENCES `SENIOR` (`SENIOR_ID`);

--
-- 테이블의 제약사항 `schedule`
--
ALTER TABLE `schedule`
  ADD CONSTRAINT `FKp5x0msimvyjoc19bcwtvwbeoy` FOREIGN KEY (`senior_id`) REFERENCES `senior` (`senior_id`);

--
-- 테이블의 제약사항 `speaker`
--
ALTER TABLE `speaker`
  ADD CONSTRAINT `FKd4frvmv2n2kyfyq35m63i9ye7` FOREIGN KEY (`senior_id`) REFERENCES `senior` (`senior_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
