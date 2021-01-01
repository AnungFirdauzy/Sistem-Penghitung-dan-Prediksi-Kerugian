-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 01 Jan 2021 pada 22.50
-- Versi server: 10.4.17-MariaDB
-- Versi PHP: 8.0.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `database_pbo`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `akun`
--

CREATE TABLE `akun` (
  `username` varchar(15) NOT NULL,
  `password` varchar(15) NOT NULL,
  `ID_pegawai` int(3) NOT NULL,
  `ID_role` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `barang`
--

CREATE TABLE `barang` (
  `ID_barang` int(3) NOT NULL,
  `nama_barang` text NOT NULL,
  `kode_barcode` int(12) NOT NULL,
  `harga_jual` int(10) NOT NULL,
  `harga_beli` int(10) NOT NULL,
  `status_barang` enum('0','1','','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `data_display`
--

CREATE TABLE `data_display` (
  `ID_barang` int(11) NOT NULL,
  `stok_display` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `data_gudang`
--

CREATE TABLE `data_gudang` (
  `ID_barang` int(3) NOT NULL,
  `stok_gudang` int(5) NOT NULL,
  `tgl_jatuh_tempo` date NOT NULL,
  `ID_supplier` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `order`
--

CREATE TABLE `order` (
  `ID_order` int(11) NOT NULL,
  `tgl_order` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `order_detail`
--

CREATE TABLE `order_detail` (
  `ID_order` int(3) NOT NULL,
  `ID_barang` int(3) NOT NULL,
  `quantity` int(5) NOT NULL,
  `total_biaya` int(10) NOT NULL,
  `pembayaran` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `pegawai`
--

CREATE TABLE `pegawai` (
  `ID_pegawai` int(3) NOT NULL,
  `nama_depan` text NOT NULL,
  `nama_belakang` text NOT NULL,
  `alamat` text NOT NULL,
  `email` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `role_table`
--

CREATE TABLE `role_table` (
  `ID_role` int(2) NOT NULL,
  `role_name` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier`
--

CREATE TABLE `supplier` (
  `ID_supplier` int(3) NOT NULL,
  `nama` text NOT NULL,
  `alamat` text NOT NULL,
  `contact_person` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `akun`
--
ALTER TABLE `akun`
  ADD PRIMARY KEY (`username`),
  ADD UNIQUE KEY `ID_pegawai` (`ID_pegawai`),
  ADD UNIQUE KEY `ID_role` (`ID_role`);

--
-- Indeks untuk tabel `barang`
--
ALTER TABLE `barang`
  ADD PRIMARY KEY (`ID_barang`);

--
-- Indeks untuk tabel `data_display`
--
ALTER TABLE `data_display`
  ADD UNIQUE KEY `ID_barang` (`ID_barang`);

--
-- Indeks untuk tabel `data_gudang`
--
ALTER TABLE `data_gudang`
  ADD UNIQUE KEY `ID_barang` (`ID_barang`),
  ADD UNIQUE KEY `ID_supplier` (`ID_supplier`);

--
-- Indeks untuk tabel `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`ID_order`);

--
-- Indeks untuk tabel `order_detail`
--
ALTER TABLE `order_detail`
  ADD UNIQUE KEY `ID_order` (`ID_order`),
  ADD UNIQUE KEY `ID_barang` (`ID_barang`);

--
-- Indeks untuk tabel `pegawai`
--
ALTER TABLE `pegawai`
  ADD PRIMARY KEY (`ID_pegawai`);

--
-- Indeks untuk tabel `role_table`
--
ALTER TABLE `role_table`
  ADD PRIMARY KEY (`ID_role`);

--
-- Indeks untuk tabel `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`ID_supplier`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `barang`
--
ALTER TABLE `barang`
  MODIFY `ID_barang` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `order`
--
ALTER TABLE `order`
  MODIFY `ID_order` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `pegawai`
--
ALTER TABLE `pegawai`
  MODIFY `ID_pegawai` int(3) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `role_table`
--
ALTER TABLE `role_table`
  MODIFY `ID_role` int(2) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `supplier`
--
ALTER TABLE `supplier`
  MODIFY `ID_supplier` int(3) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `akun`
--
ALTER TABLE `akun`
  ADD CONSTRAINT `akun_ibfk_1` FOREIGN KEY (`ID_pegawai`) REFERENCES `pegawai` (`ID_pegawai`),
  ADD CONSTRAINT `akun_ibfk_2` FOREIGN KEY (`ID_role`) REFERENCES `role_table` (`ID_role`);

--
-- Ketidakleluasaan untuk tabel `data_display`
--
ALTER TABLE `data_display`
  ADD CONSTRAINT `data_display_ibfk_1` FOREIGN KEY (`ID_barang`) REFERENCES `barang` (`ID_barang`);

--
-- Ketidakleluasaan untuk tabel `data_gudang`
--
ALTER TABLE `data_gudang`
  ADD CONSTRAINT `data_gudang_ibfk_1` FOREIGN KEY (`ID_barang`) REFERENCES `barang` (`ID_barang`),
  ADD CONSTRAINT `data_gudang_ibfk_2` FOREIGN KEY (`ID_supplier`) REFERENCES `supplier` (`ID_supplier`);

--
-- Ketidakleluasaan untuk tabel `order_detail`
--
ALTER TABLE `order_detail`
  ADD CONSTRAINT `order_detail_ibfk_1` FOREIGN KEY (`ID_order`) REFERENCES `order` (`ID_order`),
  ADD CONSTRAINT `order_detail_ibfk_2` FOREIGN KEY (`ID_barang`) REFERENCES `barang` (`ID_barang`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
