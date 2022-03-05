-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Mar 05, 2022 at 06:16 PM
-- Server version: 8.0.25-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `IOU_DB`
--

-- --------------------------------------------------------

--
-- Table structure for table `EVENT_TABLE`
--

CREATE TABLE `EVENT_TABLE` (
  `UserName` varchar(69) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `USERNAME`
--

CREATE TABLE `USERNAME` (
  `UserName` varchar(69) NOT NULL,
  `FirstName` varchar(69) DEFAULT NULL,
  `LastName` varchar(69) DEFAULT NULL,
  `Email` varchar(420) DEFAULT NULL,
  `Password` varchar(69) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `USERNAME`
--

INSERT INTO `USERNAME` (`UserName`, `FirstName`, `LastName`, `Email`, `Password`) VALUES
('noahf', 'Noah', 'Franz', 'noahfranz13@gmail.com', '12345');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `EVENT_TABLE`
--
ALTER TABLE `EVENT_TABLE`
  ADD KEY `UserName` (`UserName`);

--
-- Indexes for table `USERNAME`
--
ALTER TABLE `USERNAME`
  ADD PRIMARY KEY (`UserName`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `EVENT_TABLE`
--
ALTER TABLE `EVENT_TABLE`
  ADD CONSTRAINT `EVENT_TABLE_ibfk_1` FOREIGN KEY (`UserName`) REFERENCES `USERNAME` (`UserName`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
