-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 06, 2024 at 09:33 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_simulasi`
--

-- --------------------------------------------------------

--
-- Table structure for table `data_pemesanan`
--

CREATE TABLE `data_pemesanan` (
  `id` int(11) NOT NULL,
  `ID_Pemesanan` varchar(255) DEFAULT NULL,
  `ID_Simulasi` varchar(255) DEFAULT NULL,
  `Kode_Suku_Cadang` varchar(255) DEFAULT NULL,
  `Tanggal` datetime DEFAULT NULL,
  `ID_Supplier` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `data_permintaan`
--

CREATE TABLE `data_permintaan` (
  `id` int(11) NOT NULL,
  `Kode_Material` varchar(255) DEFAULT NULL,
  `Nama_Material` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `Tahun` year(4) DEFAULT NULL,
  `Bulan` int(11) DEFAULT NULL,
  `Permintaan` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `data_permintaan`
--

INSERT INTO `data_permintaan` (`id`, `Kode_Material`, `Nama_Material`, `Tahun`, `Bulan`, `Permintaan`) VALUES
(1, '6005631', 'Roda KRL Type KUR 12313', 2020, 1, 0),
(2, '6005631', 'Roda KRL Type KUR 12313', 2020, 2, 24),
(3, '6005631', 'Roda KRL Type KUR 12313', 2020, 3, 33),
(4, '6005631', 'Roda KRL Type KUR 12313', 2020, 4, 32),
(5, '6005631', 'Roda KRL Type KUR 12313', 2020, 5, 16),
(6, '6005631', 'Roda KRL Type KUR 12313', 2020, 6, 8),
(7, '6005631', 'Roda KRL Type KUR 12313', 2020, 7, 24),
(8, '6005631', 'Roda KRL Type KUR 12313', 2020, 8, 40),
(9, '6005631', 'Roda KRL Type KUR 12313', 2020, 9, 8),
(10, '6005631', 'Roda KRL Type KUR 12313', 2020, 10, 0),
(11, '6005631', 'Roda KRL Type KUR 12313', 2020, 11, 56),
(12, '6005631', 'Roda KRL Type KUR 12313', 2020, 12, 56),
(13, '6005631', 'Roda KRL Type KUR 12313', 2021, 1, 56),
(14, '6005631', 'Roda KRL Type KUR 12313', 2021, 2, 24),
(15, '6005631', 'Roda KRL Type KUR 12313', 2021, 3, 40),
(16, '6005631', 'Roda KRL Type KUR 12313', 2021, 4, 8),
(17, '6005631', 'Roda KRL Type KUR 12313', 2021, 5, 32),
(18, '6005631', 'Roda KRL Type KUR 12313', 2021, 6, 8),
(19, '6005631', 'Roda KRL Type KUR 12313', 2021, 7, 24),
(20, '6005631', 'Roda KRL Type KUR 12313', 2021, 8, 32),
(21, '6005631', 'Roda KRL Type KUR 12313', 2021, 9, 16),
(22, '6005631', 'Roda KRL Type KUR 12313', 2021, 10, 24),
(23, '6005631', 'Roda KRL Type KUR 12313', 2021, 11, 24),
(24, '6005631', 'Roda KRL Type KUR 12313', 2021, 12, 16),
(25, '6005632', 'Roda KRL Type KUR 12314', 2020, 1, 48),
(26, '6005632', 'Roda KRL Type KUR 12314', 2020, 2, 80),
(27, '6005632', 'Roda KRL Type KUR 12314', 2020, 3, 32),
(28, '6005632', 'Roda KRL Type KUR 12314', 2020, 4, 51),
(29, '6005632', 'Roda KRL Type KUR 12314', 2020, 5, 32),
(30, '6005632', 'Roda KRL Type KUR 12314', 2020, 6, 48),
(31, '6005632', 'Roda KRL Type KUR 12314', 2020, 7, 32),
(32, '6005632', 'Roda KRL Type KUR 12314', 2020, 8, 32),
(33, '6005632', 'Roda KRL Type KUR 12314', 2020, 9, 66),
(34, '6005632', 'Roda KRL Type KUR 12314', 2020, 10, 33),
(35, '6005632', 'Roda KRL Type KUR 12314', 2020, 11, 49),
(36, '6005632', 'Roda KRL Type KUR 12314', 2020, 12, 16),
(37, '6005632', 'Roda KRL Type KUR 12314', 2021, 1, 48),
(38, '6005632', 'Roda KRL Type KUR 12314', 2021, 2, 8),
(39, '6005632', 'Roda KRL Type KUR 12314', 2021, 3, 88),
(40, '6005632', 'Roda KRL Type KUR 12314', 2021, 4, 64),
(41, '6005632', 'Roda KRL Type KUR 12314', 2021, 5, 0),
(42, '6005632', 'Roda KRL Type KUR 12314', 2021, 6, 32),
(43, '6005632', 'Roda KRL Type KUR 12314', 2021, 7, 32),
(44, '6005632', 'Roda KRL Type KUR 12314', 2021, 8, 48),
(45, '6005632', 'Roda KRL Type KUR 12314', 2021, 9, 48),
(46, '6005632', 'Roda KRL Type KUR 12314', 2021, 10, 17),
(47, '6005632', 'Roda KRL Type KUR 12314', 2021, 11, 48),
(48, '6005632', 'Roda KRL Type KUR 12314', 2021, 12, 20),
(49, '6002976', 'Bellows bogie', 2021, 1, 0),
(50, '6002976', 'Bellows bogie', 2021, 2, 0),
(51, '6002976', 'Bellows bogie', 2021, 3, 0),
(52, '6002976', 'Bellows bogie', 2021, 4, 0),
(53, '6002976', 'Bellows bogie', 2021, 5, 4),
(54, '6002976', 'Bellows bogie', 2021, 6, 0),
(55, '6002976', 'Bellows bogie', 2021, 7, 0),
(56, '6002976', 'Bellows bogie', 2021, 8, 0),
(57, '6002976', 'Bellows bogie', 2021, 9, 20),
(58, '6002976', 'Bellows bogie', 2021, 10, 4),
(59, '6002976', 'Bellows bogie', 2021, 11, 36),
(60, '6002976', 'Bellows bogie', 2021, 12, 20),
(61, '5000034', 'RORED HDA 90', 2020, 1, 153),
(62, '5000034', 'RORED HDA 90', 2020, 2, 243),
(63, '5000034', 'RORED HDA 90', 2020, 3, 72),
(64, '5000034', 'RORED HDA 90', 2020, 4, 72),
(65, '5000034', 'RORED HDA 90', 2020, 5, 9),
(66, '5000034', 'RORED HDA 90', 2020, 6, 9),
(67, '5000034', 'RORED HDA 90', 2020, 7, 0),
(68, '5000034', 'RORED HDA 90', 2020, 8, 36),
(69, '5000034', 'RORED HDA 90', 2020, 9, 72),
(70, '5000034', 'RORED HDA 90', 2020, 10, 36),
(71, '5000034', 'RORED HDA 90', 2020, 11, 0),
(72, '5000034', 'RORED HDA 90', 2020, 12, 36),
(73, '5000034', 'RORED HDA 90', 2021, 1, 0),
(74, '5000034', 'RORED HDA 90', 2021, 2, 0),
(75, '5000034', 'RORED HDA 90', 2021, 3, 0),
(76, '5000034', 'RORED HDA 90', 2021, 4, 0),
(77, '5000034', 'RORED HDA 90', 2021, 5, 78),
(78, '5000034', 'RORED HDA 90', 2021, 6, 3),
(79, '5000034', 'RORED HDA 90', 2021, 7, 36),
(80, '5000034', 'RORED HDA 90', 2021, 8, 108),
(81, '5000034', 'RORED HDA 90', 2021, 9, 0),
(82, '5000034', 'RORED HDA 90', 2021, 10, 0),
(83, '5000034', 'RORED HDA 90', 2021, 11, 72),
(84, '5000034', 'RORED HDA 90', 2021, 12, 36),
(85, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 1, 4),
(86, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 2, 6),
(87, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 3, 11),
(88, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 4, 3),
(89, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 5, 2),
(90, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 6, 2),
(91, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 7, 0),
(92, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 8, 1),
(93, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 9, 2),
(94, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 10, 1),
(95, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 11, 4),
(96, '6003405', 'Arapen RB 320 @15,8 kg', 2020, 12, 1),
(97, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 1, 2),
(98, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 2, 1),
(99, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 3, 1),
(100, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 4, 3),
(101, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 5, 1),
(102, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 6, 0),
(103, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 7, 1),
(104, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 8, 0),
(105, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 9, 1),
(106, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 10, 1),
(107, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 11, 0),
(108, '6003405', 'Arapen RB 320 @15,8 kg', 2021, 12, 1),
(109, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 1, 69),
(110, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 2, 44),
(111, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 3, 72),
(112, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 4, 0),
(113, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 5, 0),
(114, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 6, 0),
(115, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 7, 0),
(116, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 8, 0),
(117, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 9, 0),
(118, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 10, 0),
(119, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 11, 0),
(120, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 2021, 12, 0),
(121, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 1, 0),
(122, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 2, 0),
(123, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 3, 0),
(124, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 4, 0),
(125, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 5, 0),
(126, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 6, 0),
(127, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 7, 0),
(128, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 8, 0),
(129, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 9, 0),
(130, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 10, 0),
(131, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 11, 0),
(132, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2020, 12, 50),
(133, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 1, 46),
(134, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 2, 0),
(135, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 3, 0),
(136, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 4, 0),
(137, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 5, 0),
(138, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 6, 0),
(139, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 7, 0),
(140, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 8, 0),
(141, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 9, 0),
(142, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 10, 0),
(143, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 11, 0),
(144, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 2021, 12, 20);

-- --------------------------------------------------------

--
-- Table structure for table `hasil_simulasi`
--

CREATE TABLE `hasil_simulasi` (
  `id` int(11) NOT NULL,
  `Kode_Material` varchar(255) DEFAULT NULL,
  `Hasil_Perbandingan` varchar(255) DEFAULT NULL,
  `Total_Cost` varchar(255) DEFAULT NULL,
  `Total_Service` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `hasil_simulasi`
--

INSERT INTO `hasil_simulasi` (`id`, `Kode_Material`, `Hasil_Perbandingan`, `Total_Cost`, `Total_Service`) VALUES
(2, 'Roda KRL Type KUR 12314', 'Perusahaan', 'Rp9.317.736.990,00', 1),
(4, 'Roda KRL Type KUR 12314', 'Perusahaan', 'Rp8.524.652.826,00', 1),
(5, 'Roda KRL Type KUR 12314', 'Perusahaan', 'Rp9.325.151.658,00', 1),
(6, 'Roda KRL Type KUR 12313', 'Perusahaan', 'Rp6.770.780.829,00', 1),
(7, 'RORED HDA 90', 'CR(s,Q)', 'Rp23.290.710,00', 1),
(8, 'RORED HDA 90', 'CR(s,Q)', 'Rp18.478.010,00', 1),
(9, 'Bellows bogie', 'Perusahaan', 'Rp654.777.474,00', 1),
(10, 'Bellows bogie', 'Perusahaan', 'Rp1.042.367.392,00', 1),
(11, 'Relay Omron H3CR-A8;100-240 VAC', 'Perusahaan', 'Rp40.283.445,00', 1),
(12, 'Relay Omron H3CR-A8;100-240 VAC', 'Perusahaan', 'Rp32.603.850,00', 1),
(13, 'Roda KRL Type KUR 12314', 'Perusahaan', 'Rp9.881.726.970,00', 1),
(14, 'Roda KRL Type KUR 12314', 'Perusahaan', 'Rp9.206.136.750,00', 1),
(15, 'Contactor ST-35;100 VAC/60HZ,ith 60A', 'Perusahaan', 'Rp20.989.690,00', 1),
(16, 'Roda KRL Type KUR 12313', 'Perusahaan', 'Rp5.438.198.276,00', 1),
(17, 'Bellows bogie', 'CR(s,Q)', 'Rp816.914.598,00', 1),
(18, 'Relay Omron H3CR-A8;100-240 VAC', 'CR(s,Q)', 'Rp58.714.110,00', 1),
(19, 'Relay Omron H3CR-A8;100-240 VAC', 'Perusahaan', 'Rp40.165.635,00', 1),
(20, 'Roda KRL Type KUR 12313', 'Perusahaan', 'Rp5.972.733.285,00', 1),
(21, 'Roda KRL Type KUR 12314', 'Perusahaan', 'Rp10.115.764.266,00', 1),
(22, 'RORED HDA 90', 'CR(s,Q)', 'Rp20.423.140,00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `suku_cadang`
--

CREATE TABLE `suku_cadang` (
  `id` int(11) NOT NULL,
  `Kode_Material` varchar(255) DEFAULT NULL,
  `Nama_Material` varchar(255) DEFAULT NULL,
  `Harga_Material` bigint(20) DEFAULT NULL,
  `Biaya_Pemesanan` bigint(20) DEFAULT NULL,
  `Biaya_Penyimpanan` bigint(20) DEFAULT NULL,
  `Biaya_Stockout` bigint(20) DEFAULT NULL,
  `Leadtime` float NOT NULL,
  `Stok` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `suku_cadang`
--

INSERT INTO `suku_cadang` (`id`, `Kode_Material`, `Nama_Material`, `Harga_Material`, `Biaya_Pemesanan`, `Biaya_Penyimpanan`, `Biaya_Stockout`, `Leadtime`, `Stok`) VALUES
(1, '6005631', 'Roda KRL Type KUR 12313', 19012449, 22500, 1235809, 533200, 3, '125'),
(2, '6005632', 'Roda KRL Type KUR 12314', 19011966, 22500, 1235778, 533200, 3, '164'),
(3, '6002976', 'Bellows bogie', 11240524, 22500, 808842, 473000, 12, '69'),
(4, '5000034', 'RORED HDA 90', 37690, 22500, 2450, 43000, 1, '10'),
(5, '6003405', 'Arapen RB 320 @15,8 kg', 2135539, 22500, 138810, 43000, 1, '23'),
(6, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', 231000, 22500, 15015, 172000, 1.71429, '70'),
(7, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', 566000, 22500, 36790, 197800, 0.857143, '51');

-- --------------------------------------------------------

--
-- Table structure for table `supplier`
--

CREATE TABLE `supplier` (
  `id` int(11) NOT NULL,
  `Kode_Material` varchar(255) DEFAULT NULL,
  `Nama_Material` varchar(255) DEFAULT NULL,
  `ID_Supplier` varchar(255) DEFAULT NULL,
  `Nama_Supplier` varchar(255) DEFAULT NULL,
  `Alamat_Supplier` varchar(255) DEFAULT NULL,
  `Contact_Supplier` varchar(255) DEFAULT NULL,
  `Email_Contact` varchar(255) DEFAULT NULL,
  `Contact_Name` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `supplier`
--

INSERT INTO `supplier` (`id`, `Kode_Material`, `Nama_Material`, `ID_Supplier`, `Nama_Supplier`, `Alamat_Supplier`, `Contact_Supplier`, `Email_Contact`, `Contact_Name`) VALUES
(1, '6005631', 'Roda KRL Type KUR 12313', '210075', 'SUMITOMO CORPORATION', 'East Tower 3-2 Otemachi 2-chome, Chiyoda-ku, Tokyo, Tokyo 100-8601, Japan', '62-21-5251550', 'name@sumitomocorp.com', 'Masayuki'),
(2, '6005632', 'Roda KRL Type KUR 12314', '210075', 'SUMITOMO CORPORATION', 'East Tower 3-2 Otemachi 2-chome, Chiyoda-ku, Tokyo, Tokyo 100-8601, Japan', '62-21-5251550', 'name@sumitomocorp.com', 'Masayuki'),
(3, '6002976', 'Bellows bogie', '210065', 'JR EAST RAILCAR TECH. & MAINTENANCE', '2-2-2 Yoyogi, Shibuya-ku, Tokyo, Japan', '(81)-3-5334-1151', 'name@jreast.com', 'Tetsuro'),
(4, '5000034', 'RORED HDA 90', '200125', 'PT. RESKA MULTI USAHA', 'Stasiun Mangga Besar Lantai Dasar Jl. Karang Anyar No.1 Jakarta Pusat 10740', '(021)-623-02540', 'humas@reska.co.id', 'Reska'),
(5, '6003405', 'Arapen RB 320 @15,8 kg', '200162', 'PT. SARI SARANA KIMIATAMA', 'Jl. Daan Mogot Km 11, Cengkareng, Jakarta 11710, Indonesia', '62-21-540-2211', 'info@ssktama.com', 'Sari'),
(6, '6005801', 'Relay Omron H3CR-A8;100-240 VAC', '200133', 'PT. GJ INTERNATIONAL', 'Gedung Wisma Nugra Sanatana Lt. 11 Jl. Jend. Sudirman Kav. 7-8 Kel. Karet Tengsin Kec. Tanah Abang', '62-21-570-0505', 'admin@pt-gji.com', 'Endah'),
(7, '6005810', 'Contactor ST-35;100 VAC/60HZ,ith 60A', '200193', 'PT. DINAMIKA TRIMITRA SEJAHTERA', 'Botanic Junction Blok H-9 No. 7 Mega Kebon Jeruk, RT.7/RW.1, Joglo, Kec. Kembangan, Kota Jakarta Barat, Daerah Khusus Ibukota Jakarta', '(021)-29325859', '239@Yahoo.com', 'Citra');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `data_pemesanan`
--
ALTER TABLE `data_pemesanan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `data_permintaan`
--
ALTER TABLE `data_permintaan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hasil_simulasi`
--
ALTER TABLE `hasil_simulasi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `suku_cadang`
--
ALTER TABLE `suku_cadang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `data_pemesanan`
--
ALTER TABLE `data_pemesanan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `data_permintaan`
--
ALTER TABLE `data_permintaan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=145;

--
-- AUTO_INCREMENT for table `hasil_simulasi`
--
ALTER TABLE `hasil_simulasi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `suku_cadang`
--
ALTER TABLE `suku_cadang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `supplier`
--
ALTER TABLE `supplier`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
