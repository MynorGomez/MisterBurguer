-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: restaurante
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  PRIMARY KEY (`id_categoria`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Hamburguesas','Hamburguesas de la casa','activo'),(2,'Bebidas','Refrescos y bebidas','activo'),(3,'Acompañamientos','Papas y extras','activo');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `nombres` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidos` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nit` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `clientes_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,NULL,'Juan','Pérez','5555-1111','Zona 1','1234567-8','2026-03-29 17:53:44'),(2,NULL,'María','López','5555-2222','Zona 5','9876543-2','2026-03-29 17:53:44'),(3,NULL,'Carlos','Ramírez','5555-3333','Zona 10','4567891-0','2026-03-29 17:53:44');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `combo_detalle`
--

DROP TABLE IF EXISTS `combo_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `combo_detalle` (
  `id_combo_detalle` int NOT NULL AUTO_INCREMENT,
  `id_combo` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_combo_detalle`),
  KEY `idx_combo_detalle_combo` (`id_combo`),
  KEY `idx_combo_detalle_producto` (`id_producto`),
  CONSTRAINT `combo_detalle_ibfk_1` FOREIGN KEY (`id_combo`) REFERENCES `combos` (`id_combo`) ON DELETE CASCADE,
  CONSTRAINT `combo_detalle_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combo_detalle`
--

LOCK TABLES `combo_detalle` WRITE;
/*!40000 ALTER TABLE `combo_detalle` DISABLE KEYS */;
INSERT INTO `combo_detalle` VALUES (10,9,1,1.00),(11,9,2,1.00),(12,9,3,1.00),(13,8,1,2.00),(14,8,2,1.00),(15,8,3,1.00),(16,7,1,2.00),(17,7,2,2.00),(18,7,3,2.00);
/*!40000 ALTER TABLE `combo_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `combos`
--

DROP TABLE IF EXISTS `combos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `combos` (
  `id_combo` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `precio` decimal(10,2) NOT NULL,
  `imagen` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `disponible` enum('si','no') COLLATE utf8mb4_unicode_ci DEFAULT 'si',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_combo`),
  KEY `idx_combos_disponible` (`disponible`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `combos`
--

LOCK TABLES `combos` WRITE;
/*!40000 ALTER TABLE `combos` DISABLE KEYS */;
INSERT INTO `combos` VALUES (1,'Combo Clasico','Hamburguesa clasica + papas + gaseosa',15.99,'combo_clasico.jpg','si','2026-04-01 19:33:58'),(2,'Combo Familiar','2 Hamburguesas + 2 papas + 2 gaseosas',28.99,'combo_familiar.jpg','si','2026-04-01 19:33:58'),(3,'Combo Deluxe','Hamburguesa deluxe + aros de cebolla + gaseosa grande',22.99,'combo_deluxe.jpg','si','2026-04-01 19:33:58'),(7,'Combo Clásico','Hamburguesa + papas + refresco',15.99,'combo_clasico.jpg','si','2026-04-01 19:37:02'),(8,'Combo Deluxe','Hamburguesa doble + papas grandes + refresco',22.99,'combo_deluxe.jpg','si','2026-04-01 19:37:02'),(9,'Combo Familiar','2 Hamburguesas + 2 papas + 2 refrescos',28.99,'combo_familiar.jpg','si','2026-04-01 19:37:02');
/*!40000 ALTER TABLE `combos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras`
--

DROP TABLE IF EXISTS `compras`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras` (
  `id_compra` int NOT NULL AUTO_INCREMENT,
  `id_proveedor` int NOT NULL,
  `id_empleado` int NOT NULL,
  `fecha_compra` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `numero_factura` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `subtotal` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total` decimal(12,2) NOT NULL DEFAULT '0.00',
  `estado` enum('registrada','anulada') COLLATE utf8mb4_unicode_ci DEFAULT 'registrada',
  PRIMARY KEY (`id_compra`),
  KEY `id_proveedor` (`id_proveedor`),
  KEY `id_empleado` (`id_empleado`),
  CONSTRAINT `compras_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `compras_ibfk_2` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras`
--

LOCK TABLES `compras` WRITE;
/*!40000 ALTER TABLE `compras` DISABLE KEYS */;
INSERT INTO `compras` VALUES (1,4,1,'2026-04-09 00:00:00','COM-01',205.00,205.00,'registrada'),(2,5,1,'2026-04-07 00:00:00','COM-01',506.00,506.00,'registrada');
/*!40000 ALTER TABLE `compras` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras_detalle`
--

DROP TABLE IF EXISTS `compras_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras_detalle` (
  `id_compra_detalle` int NOT NULL AUTO_INCREMENT,
  `id_compra` int NOT NULL,
  `id_insumo` int NOT NULL,
  `cantidad` decimal(12,2) NOT NULL,
  `costo_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id_compra_detalle`),
  KEY `id_compra` (`id_compra`),
  KEY `id_insumo` (`id_insumo`),
  CONSTRAINT `compras_detalle_ibfk_1` FOREIGN KEY (`id_compra`) REFERENCES `compras` (`id_compra`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `compras_detalle_ibfk_2` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras_detalle`
--

LOCK TABLES `compras_detalle` WRITE;
/*!40000 ALTER TABLE `compras_detalle` DISABLE KEYS */;
INSERT INTO `compras_detalle` VALUES (1,1,1,10.00,20.50,205.00),(2,2,1,20.00,25.30,506.00);
/*!40000 ALTER TABLE `compras_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleados`
--

DROP TABLE IF EXISTS `empleados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleados` (
  `id_empleado` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `nombres` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `apellidos` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dpi` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `puesto` varchar(80) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `salario` decimal(10,2) DEFAULT NULL,
  `fecha_contratacion` date DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  PRIMARY KEY (`id_empleado`),
  UNIQUE KEY `id_usuario` (`id_usuario`),
  UNIQUE KEY `dpi` (`dpi`),
  CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleados`
--

LOCK TABLES `empleados` WRITE;
/*!40000 ALTER TABLE `empleados` DISABLE KEYS */;
INSERT INTO `empleados` VALUES (1,1,'Admin','Principal','1234567890101','55555555','Ciudad','Administrador',5000.00,'2026-03-24','activo'),(2,2,'Luis','Castro','788346','980374589','Guatemala','3',4522.00,'2026-03-18','activo');
/*!40000 ALTER TABLE `empleados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ingredientes`
--

DROP TABLE IF EXISTS `ingredientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ingredientes` (
  `id_ingrediente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `precio_extra` decimal(10,2) DEFAULT '0.00',
  `id_insumo` int DEFAULT NULL,
  `disponible` enum('si','no') COLLATE utf8mb4_unicode_ci DEFAULT 'si',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_ingrediente`),
  KEY `id_insumo` (`id_insumo`),
  KEY `idx_ingredientes_disponible` (`disponible`),
  CONSTRAINT `ingredientes_ibfk_1` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ingredientes`
--

LOCK TABLES `ingredientes` WRITE;
/*!40000 ALTER TABLE `ingredientes` DISABLE KEYS */;
INSERT INTO `ingredientes` VALUES (1,'Queso Extra','Porción adicional de queso cheddar',1.50,NULL,'si','2026-04-01 19:37:02'),(2,'Bacon','Tiras de bacon crujiente',2.00,NULL,'si','2026-04-01 19:37:02'),(3,'Huevo','Huevo frito',1.00,NULL,'si','2026-04-01 19:37:02'),(4,'Cebolla Caramelizada','Cebolla caramelizada',1.50,NULL,'si','2026-04-01 19:37:02'),(5,'Champiñones','Champiñones salteados',1.50,NULL,'si','2026-04-01 19:37:02'),(6,'Guacamole','Guacamole fresco',2.50,NULL,'si','2026-04-01 19:37:02'),(7,'Salsa BBQ','Salsa barbacoa',0.50,NULL,'si','2026-04-01 19:37:02'),(8,'Salsa Picante','Salsa picante',0.50,NULL,'si','2026-04-01 19:37:02');
/*!40000 ALTER TABLE `ingredientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumos`
--

DROP TABLE IF EXISTS `insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumos` (
  `id_insumo` int NOT NULL AUTO_INCREMENT,
  `id_unidad` int NOT NULL,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `stock_actual` decimal(12,2) NOT NULL DEFAULT '0.00',
  `stock_minimo` decimal(12,2) NOT NULL DEFAULT '0.00',
  `costo_referencia` decimal(10,2) DEFAULT '0.00',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  PRIMARY KEY (`id_insumo`),
  UNIQUE KEY `nombre` (`nombre`),
  KEY `id_unidad` (`id_unidad`),
  CONSTRAINT `insumos_ibfk_1` FOREIGN KEY (`id_unidad`) REFERENCES `unidades_medida` (`id_unidad`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumos`
--

LOCK TABLES `insumos` WRITE;
/*!40000 ALTER TABLE `insumos` DISABLE KEYS */;
INSERT INTO `insumos` VALUES (1,3,'Carne de res',NULL,8371.00,2000.00,0.05,'activo'),(2,1,'Pan de hamburguesa',NULL,189.00,50.00,1.00,'activo'),(3,2,'Queso',NULL,4935.00,1000.00,0.03,'activo'),(4,2,'Lechuga',NULL,2814.00,500.00,0.02,'activo'),(5,2,'Tomate',NULL,2815.00,500.00,0.02,'activo'),(6,4,'Salsa ketchup',NULL,1994.00,500.00,0.01,'activo'),(7,3,'Papas',NULL,10000.00,2000.00,0.02,'activo');
/*!40000 ALTER TABLE `insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `movimientos_inventario`
--

DROP TABLE IF EXISTS `movimientos_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `movimientos_inventario` (
  `id_movimiento` int NOT NULL AUTO_INCREMENT,
  `id_insumo` int NOT NULL,
  `tipo_movimiento` enum('entrada_compra','salida_venta','ajuste_entrada','ajuste_salida') COLLATE utf8mb4_unicode_ci NOT NULL,
  `cantidad` decimal(12,2) NOT NULL,
  `referencia` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `observacion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fecha_movimiento` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_movimiento`),
  KEY `id_insumo` (`id_insumo`),
  CONSTRAINT `movimientos_inventario_ibfk_1` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `movimientos_inventario`
--

LOCK TABLES `movimientos_inventario` WRITE;
/*!40000 ALTER TABLE `movimientos_inventario` DISABLE KEYS */;
INSERT INTO `movimientos_inventario` VALUES (1,1,'salida_venta',150.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(2,2,'salida_venta',1.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(3,4,'salida_venta',20.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(4,5,'salida_venta',20.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(5,1,'salida_venta',150.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(6,2,'salida_venta',1.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(7,3,'salida_venta',30.00,'PED-20260329122346','Descuento por pedido web','2026-03-29 12:23:46'),(8,1,'salida_venta',300.00,'PED-20260329122604','Descuento por pedido web','2026-03-29 12:26:04'),(9,2,'salida_venta',2.00,'PED-20260329122604','Descuento por pedido web','2026-03-29 12:26:04'),(10,4,'salida_venta',40.00,'PED-20260329122604','Descuento por pedido web','2026-03-29 12:26:04'),(11,5,'salida_venta',40.00,'PED-20260329122604','Descuento por pedido web','2026-03-29 12:26:04'),(12,1,'salida_venta',150.00,'PED-20260329194844','Descuento por pedido web','2026-03-29 19:48:44'),(13,2,'salida_venta',1.00,'PED-20260329194844','Descuento por pedido web','2026-03-29 19:48:44'),(14,4,'salida_venta',20.00,'PED-20260329194844','Descuento por pedido web','2026-03-29 19:48:44'),(15,5,'salida_venta',20.00,'PED-20260329194844','Descuento por pedido web','2026-03-29 19:48:44'),(16,1,'salida_venta',150.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(17,2,'salida_venta',1.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(18,4,'salida_venta',20.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(19,5,'salida_venta',20.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(20,1,'salida_venta',150.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(21,2,'salida_venta',1.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(22,3,'salida_venta',30.00,'PED-20260329200148','Descuento por pedido web','2026-03-29 20:01:48'),(23,1,'salida_venta',150.00,'PED-20260329201059','Descuento por pedido web','2026-03-29 20:10:59'),(24,2,'salida_venta',1.00,'PED-20260329201059','Descuento por pedido web','2026-03-29 20:10:59'),(25,4,'salida_venta',20.00,'PED-20260329201059','Descuento por pedido web','2026-03-29 20:10:59'),(26,5,'salida_venta',20.00,'PED-20260329201059','Descuento por pedido web','2026-03-29 20:10:59'),(27,1,'salida_venta',150.00,'PED-20260329210131','Descuento por pedido web','2026-03-29 21:01:31'),(28,2,'salida_venta',1.00,'PED-20260329210131','Descuento por pedido web','2026-03-29 21:01:31'),(29,4,'salida_venta',20.00,'PED-20260329210131','Descuento por pedido web','2026-03-29 21:01:31'),(30,5,'salida_venta',20.00,'PED-20260329210131','Descuento por pedido web','2026-03-29 21:01:31'),(31,1,'salida_venta',150.00,'PED-20260330214327','Descuento por pedido web','2026-03-30 21:43:27'),(32,2,'salida_venta',1.00,'PED-20260330214327','Descuento por pedido web','2026-03-30 21:43:28'),(33,4,'salida_venta',20.00,'PED-20260330214327','Descuento por pedido web','2026-03-30 21:43:28'),(34,5,'salida_venta',20.00,'PED-20260330214327','Descuento por pedido web','2026-03-30 21:43:28'),(35,1,'salida_venta',150.00,'PED-20260330221111','Descuento por pedido web','2026-03-30 22:11:11'),(36,2,'salida_venta',1.00,'PED-20260330221111','Descuento por pedido web','2026-03-30 22:11:11'),(37,4,'salida_venta',20.00,'PED-20260330221111','Descuento por pedido web','2026-03-30 22:11:11'),(38,5,'salida_venta',20.00,'PED-20260330221111','Descuento por pedido web','2026-03-30 22:11:11'),(39,1,'salida_venta',1.00,'PED-20260401155233','Descuento carne personalizado','2026-04-01 15:52:33'),(40,1,'salida_venta',1.00,'PED-20260401155302','Descuento carne personalizado','2026-04-01 15:53:02'),(41,1,'salida_venta',1.00,'PED-20260401155808','Descuento carne personalizado','2026-04-01 15:58:08'),(42,3,'salida_venta',1.00,'PED-20260401155808','Descuento ingrediente personalizado','2026-04-01 15:58:08'),(43,4,'salida_venta',1.00,'PED-20260401155808','Descuento ingrediente personalizado','2026-04-01 15:58:08'),(44,5,'salida_venta',1.00,'PED-20260401155808','Descuento ingrediente personalizado','2026-04-01 15:58:08'),(45,6,'salida_venta',1.00,'PED-20260401155808','Descuento ingrediente personalizado','2026-04-01 15:58:08'),(46,1,'salida_venta',1.00,'PED-20260401155837','Descuento carne personalizado','2026-04-01 15:58:37'),(47,3,'salida_venta',1.00,'PED-20260401155837','Descuento ingrediente personalizado','2026-04-01 15:58:37'),(48,4,'salida_venta',1.00,'PED-20260401155837','Descuento ingrediente personalizado','2026-04-01 15:58:37'),(49,5,'salida_venta',1.00,'PED-20260401155837','Descuento ingrediente personalizado','2026-04-01 15:58:37'),(50,6,'salida_venta',1.00,'PED-20260401155837','Descuento ingrediente personalizado','2026-04-01 15:58:37'),(51,1,'salida_venta',1.00,'PED-20260401184904','Descuento carne personalizado','2026-04-01 18:49:04'),(52,1,'entrada_compra',10.00,'COM-01','Entrada por compra','2026-04-01 19:39:03'),(53,1,'entrada_compra',20.00,'COM-01','Entrada por compra','2026-04-01 19:40:25'),(54,1,'salida_venta',1.00,'PED-20260401195418','Descuento carne personalizado','2026-04-01 19:54:18'),(55,4,'salida_venta',1.00,'PED-20260401195418','Descuento ingrediente personalizado','2026-04-01 19:54:18'),(56,5,'salida_venta',1.00,'PED-20260401195418','Descuento ingrediente personalizado','2026-04-01 19:54:18'),(57,6,'salida_venta',1.00,'PED-20260401195418','Descuento ingrediente personalizado','2026-04-01 19:54:18'),(58,1,'salida_venta',1.00,'PED-20260401210855','Descuento carne personalizado','2026-04-01 21:08:55'),(59,3,'salida_venta',1.00,'PED-20260401210855','Descuento ingrediente personalizado','2026-04-01 21:08:55'),(60,4,'salida_venta',1.00,'PED-20260401210855','Descuento ingrediente personalizado','2026-04-01 21:08:55'),(61,5,'salida_venta',1.00,'PED-20260401210855','Descuento ingrediente personalizado','2026-04-01 21:08:55'),(62,6,'salida_venta',1.00,'PED-20260401210855','Descuento ingrediente personalizado','2026-04-01 21:08:55'),(63,1,'salida_venta',1.00,'PED-20260408203603','Descuento carne personalizado','2026-04-08 20:36:03'),(64,3,'salida_venta',1.00,'PED-20260408203603','Descuento ingrediente personalizado','2026-04-08 20:36:03'),(65,4,'salida_venta',1.00,'PED-20260408203603','Descuento ingrediente personalizado','2026-04-08 20:36:03'),(66,6,'salida_venta',1.00,'PED-20260408203603','Descuento ingrediente personalizado','2026-04-08 20:36:03'),(67,1,'salida_venta',1.00,'PED-20260408203642','Descuento carne personalizado','2026-04-08 20:36:42'),(68,3,'salida_venta',1.00,'PED-20260408203642','Descuento ingrediente personalizado','2026-04-08 20:36:42'),(69,4,'salida_venta',1.00,'PED-20260408203642','Descuento ingrediente personalizado','2026-04-08 20:36:42'),(70,5,'salida_venta',1.00,'PED-20260408203642','Descuento ingrediente personalizado','2026-04-08 20:36:42'),(71,6,'salida_venta',1.00,'PED-20260408203642','Descuento ingrediente personalizado','2026-04-08 20:36:42');
/*!40000 ALTER TABLE `movimientos_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido_detalle`
--

DROP TABLE IF EXISTS `pedido_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido_detalle` (
  `id_pedido_detalle` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  `observaciones` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_pedido_detalle`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `pedido_detalle_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `pedido_detalle_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido_detalle`
--

LOCK TABLES `pedido_detalle` WRITE;
/*!40000 ALTER TABLE `pedido_detalle` DISABLE KEYS */;
INSERT INTO `pedido_detalle` VALUES (1,1,1,1,25.00,25.00,NULL),(2,1,5,2,15.00,30.00,NULL),(3,2,5,1,15.00,15.00,NULL),(4,3,4,1,10.00,10.00,NULL),(5,3,1,1,25.00,25.00,NULL),(6,3,2,1,30.00,30.00,NULL),(7,3,5,1,15.00,15.00,NULL),(8,4,1,2,25.00,50.00,NULL),(9,5,1,1,25.00,25.00,NULL),(10,6,5,1,15.00,15.00,NULL),(11,7,4,1,10.00,10.00,NULL),(12,8,4,4,10.00,40.00,NULL),(13,8,1,1,25.00,25.00,NULL),(14,8,2,1,30.00,30.00,NULL),(15,9,4,1,10.00,10.00,NULL),(16,10,1,1,25.00,25.00,NULL),(17,11,1,1,25.00,25.00,NULL),(18,12,4,1,10.00,10.00,NULL),(19,12,5,1,15.00,15.00,NULL),(20,13,5,1,15.00,15.00,NULL),(21,14,5,1,15.00,15.00,NULL),(22,15,5,1,15.00,15.00,NULL),(23,16,4,1,10.00,10.00,NULL),(24,17,1,1,25.00,25.00,NULL),(25,18,4,1,10.00,10.00,NULL),(26,19,4,1,10.00,10.00,NULL),(27,20,4,1,10.00,10.00,NULL),(28,21,4,1,10.00,10.00,NULL),(29,22,1,1,25.00,25.00,NULL),(30,23,1,1,15.99,15.99,NULL),(39,32,1,1,25.00,25.00,NULL),(40,33,1,1,25.00,25.00,NULL),(41,34,1,1,25.00,25.00,NULL),(42,35,1,1,25.00,25.00,NULL),(43,36,1,1,25.00,25.00,NULL),(44,37,1,1,25.00,25.00,'Ingredientes: Lechuga, Tomate, Salsa ketchup | Papas: Papas Fritas | Bebida: Coca Cola'),(45,38,1,1,25.00,25.00,'Pan: INTEGRAL | Queso: Queso | Ingredientes: Queso, Lechuga, Tomate, Salsa ketchup | Papas: Papas Fritas | Bebida: Coca Cola'),(46,39,1,1,15.99,15.99,NULL),(47,40,3,1,22.99,22.99,NULL),(48,41,1,1,15.99,15.99,NULL),(49,42,1,1,15.99,15.99,NULL),(50,43,1,1,15.99,15.99,NULL),(51,44,1,1,15.99,15.99,NULL),(52,45,1,1,15.99,15.99,NULL),(53,46,1,1,15.99,15.99,NULL),(54,47,1,1,15.99,15.99,NULL),(55,48,1,1,15.99,15.99,NULL),(56,49,1,1,15.99,15.99,NULL),(57,50,1,1,15.99,15.99,NULL),(58,51,1,1,15.99,15.99,NULL),(59,52,1,1,15.99,15.99,NULL),(60,53,1,1,15.99,15.99,NULL),(61,54,1,1,15.99,15.99,NULL),(62,55,1,1,15.99,15.99,NULL),(63,56,1,1,15.99,15.99,NULL),(64,57,1,1,25.00,25.00,'Queso: Queso | Ingredientes: Queso, Lechuga, Salsa ketchup'),(65,58,1,1,25.00,25.00,'Queso: Queso | Ingredientes: Queso, Lechuga, Tomate, Salsa ketchup | Papas: Papas Fritas | Bebida: Coca Cola');
/*!40000 ALTER TABLE `pedido_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int DEFAULT NULL,
  `nombre_cliente_invitado` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono_cliente_invitado` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_pedido` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_pedido` enum('local','llevar','domicilio','web') COLLATE utf8mb4_unicode_ci DEFAULT 'web',
  `estado` enum('pendiente','confirmado','en_preparacion','listo','entregado','cancelado') COLLATE utf8mb4_unicode_ci DEFAULT 'pendiente',
  `fecha_pedido` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `subtotal` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total` decimal(12,2) NOT NULL DEFAULT '0.00',
  `observaciones` text COLLATE utf8mb4_unicode_ci,
  `direccion_entrega` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correo_cliente_invitado` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_pedido`),
  UNIQUE KEY `numero_pedido` (`numero_pedido`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,1,NULL,NULL,'P001','local','pendiente','2026-03-29 12:10:46',0.00,55.00,NULL,NULL,NULL),(2,NULL,'Carlos','4278465','PED-20260329122302','web','entregado','2026-03-29 12:23:02',15.00,15.00,NULL,NULL,NULL),(3,NULL,'Carlos','4278465','PED-20260329122346','web','entregado','2026-03-29 12:23:46',80.00,80.00,NULL,NULL,NULL),(4,NULL,'Carlos','4278465','PED-20260329122604','web','entregado','2026-03-29 12:26:04',50.00,50.00,NULL,NULL,NULL),(5,NULL,'Carlos','4278465','PED-20260329194844','web','entregado','2026-03-29 19:48:44',25.00,25.00,NULL,NULL,NULL),(6,NULL,'Carlos','4278465','PED-20260329195003','web','entregado','2026-03-29 19:50:03',15.00,15.00,NULL,NULL,NULL),(7,NULL,'Carlos','4278465','PED-20260329195211','web','entregado','2026-03-29 19:52:11',10.00,10.00,NULL,NULL,NULL),(8,NULL,'Carlos','4278465','PED-20260329200148','web','entregado','2026-03-29 20:01:48',95.00,95.00,NULL,NULL,NULL),(9,NULL,'Carlos','4278465','PED-20260329200331','web','entregado','2026-03-29 20:03:31',10.00,10.00,NULL,NULL,NULL),(10,NULL,'Carlos','4278465','PED-20260329201059','web','entregado','2026-03-29 20:10:59',25.00,25.00,NULL,NULL,NULL),(11,NULL,'Carlos','4278465','PED-20260329210131','web','entregado','2026-03-29 21:01:31',25.00,25.00,NULL,NULL,NULL),(12,NULL,'Carlos','4278465','PED-20260330213630','web','entregado','2026-03-30 21:36:30',25.00,25.00,NULL,NULL,NULL),(13,NULL,'Carlos','4278465','PED-20260330213842','web','entregado','2026-03-30 21:38:42',15.00,15.00,NULL,NULL,NULL),(14,NULL,'Carlos','4278465','PED-20260330214152','web','entregado','2026-03-30 21:41:52',15.00,15.00,NULL,NULL,NULL),(15,NULL,'Carlos','4278465','PED-20260330214226','web','entregado','2026-03-30 21:42:26',15.00,15.00,NULL,NULL,NULL),(16,NULL,'Carlos','4278465','PED-20260330214245','web','entregado','2026-03-30 21:42:45',10.00,10.00,NULL,NULL,NULL),(17,NULL,'Carlos','4278465','PED-20260330214327','web','entregado','2026-03-30 21:43:27',25.00,25.00,NULL,NULL,NULL),(18,NULL,'Carlos','4278465','PED-20260330215757','web','entregado','2026-03-30 21:57:57',10.00,10.00,NULL,NULL,NULL),(19,NULL,'Carlos','4278465','PED-20260330215814','web','entregado','2026-03-30 21:58:14',10.00,10.00,NULL,NULL,NULL),(20,NULL,'Carlos','4278465','PED-20260330220220','web','entregado','2026-03-30 22:02:20',10.00,10.00,NULL,NULL,NULL),(21,NULL,'Carlos','4278465','PED-20260330220239','web','entregado','2026-03-30 22:02:39',10.00,10.00,NULL,NULL,NULL),(22,NULL,'Carlos','4278465','PED-20260330221111','web','entregado','2026-03-30 22:11:11',25.00,25.00,NULL,NULL,NULL),(23,NULL,'Carlos','4278465','PED-20260401134742','web','entregado','2026-04-01 13:47:42',15.99,15.99,NULL,NULL,NULL),(32,NULL,'Carlos','4278465','PED-20260401155233','web','entregado','2026-04-01 15:52:33',25.00,25.00,NULL,NULL,NULL),(33,NULL,'Carlos','4278465','PED-20260401155302','web','entregado','2026-04-01 15:53:02',25.00,25.00,NULL,NULL,NULL),(34,NULL,'Carlos','4278465','PED-20260401155808','web','entregado','2026-04-01 15:58:08',25.00,25.00,NULL,NULL,NULL),(35,NULL,'Carlos','4278465','PED-20260401155837','web','entregado','2026-04-01 15:58:37',25.00,25.00,NULL,NULL,NULL),(36,NULL,'Carlos','4278465','PED-20260401184904','web','entregado','2026-04-01 18:49:04',25.00,25.00,NULL,NULL,NULL),(37,NULL,'Carlos','4278465','PED-20260401195418','web','entregado','2026-04-01 19:54:18',25.00,25.00,NULL,NULL,NULL),(38,NULL,'Mynor','26481190','PED-20260401210855','web','entregado','2026-04-01 21:08:55',25.00,25.00,NULL,NULL,NULL),(39,NULL,'Mynor',NULL,'PED-20260402122509','web','entregado','2026-04-02 12:25:09',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(40,NULL,'Mynor',NULL,'PED-20260402123224','web','entregado','2026-04-02 12:32:24',22.99,22.99,NULL,NULL,'16mynorgomez@gmail.com'),(41,NULL,'Mynor',NULL,'PED-20260402123305','web','entregado','2026-04-02 12:33:05',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(42,NULL,'Mynor',NULL,'PED-20260402123552','web','entregado','2026-04-02 12:35:52',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(43,NULL,'Mynor',NULL,'PED-20260402123837','web','listo','2026-04-02 12:38:37',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(44,NULL,'Mynor',NULL,'PED-20260402124359','web','confirmado','2026-04-02 12:43:59',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(45,NULL,'Mynor',NULL,'PED-20260402124442','web','confirmado','2026-04-02 12:44:42',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(46,NULL,'Mynor',NULL,'PED-20260402124649','web','confirmado','2026-04-02 12:46:49',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(47,NULL,'Mynor',NULL,'PED-20260402141005','web','confirmado','2026-04-02 14:10:05',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(48,NULL,'Mynor',NULL,'PED-20260402141033','web','confirmado','2026-04-02 14:10:33',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(49,NULL,'Mynor',NULL,'PED-20260402141422','web','confirmado','2026-04-02 14:14:22',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(50,NULL,'Mynor',NULL,'PED-20260402141958','web','confirmado','2026-04-02 14:19:58',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(51,NULL,'Mynor',NULL,'PED-20260402142116','web','confirmado','2026-04-02 14:21:16',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(52,NULL,'Mynor',NULL,'PED-20260402142313','web','confirmado','2026-04-02 14:23:13',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(53,NULL,'Mynor',NULL,'PED-20260402142500','web','confirmado','2026-04-02 14:25:00',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(54,NULL,'Mynor',NULL,'PED-20260402142709','web','confirmado','2026-04-02 14:27:09',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(55,NULL,'Mynor',NULL,'PED-20260402144536','web','listo','2026-04-02 14:45:36',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(56,NULL,'Mynor',NULL,'PED-20260402150246','web','confirmado','2026-04-02 15:02:46',15.99,15.99,NULL,NULL,'16mynorgomez@gmail.com'),(57,NULL,'Cristopher Valenzuela',NULL,'PED-20260408203603','web','listo','2026-04-08 20:36:03',25.00,25.00,NULL,NULL,'cvalenzuelam3@miumg.edu.gt'),(58,NULL,'Jonathan Alonso',NULL,'PED-20260408203642','web','listo','2026-04-08 20:36:42',25.00,25.00,NULL,NULL,'alonsojonathan23@gmail.com');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `id_categoria` int NOT NULL,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `precio` decimal(10,2) NOT NULL,
  `imagen` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `tiempo_preparacion_min` int DEFAULT '10',
  `disponible` enum('si','no') COLLATE utf8mb4_unicode_ci DEFAULT 'si',
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_producto`),
  KEY `id_categoria` (`id_categoria`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,1,'Hamburguesa Clásica','Carne, pan, lechuga y tomate',25.00,NULL,10,'si','activo','2026-03-29 18:08:33'),(2,1,'Hamburguesa con Queso','Incluye queso',30.00,NULL,10,'si','activo','2026-03-29 18:08:33'),(3,1,'Hamburguesa Doble','Doble carne',40.00,NULL,10,'si','activo','2026-03-29 18:08:33'),(4,2,'Coca Cola','Bebida gaseosa',10.00,NULL,10,'si','activo','2026-03-29 18:08:33'),(5,3,'Papas Fritas','Porción de papas',15.00,'papas.png',10,'si','activo','2026-03-29 18:08:33');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `contacto_nombre` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `correo` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `direccion` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nit` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (4,'PATITOS S.A','Oscar Gonzalez','980374589','akl@prueba','Guatemala','0978874','activo'),(5,'Carnes Premium',NULL,'5555-6666',NULL,'Zona 12','111111-1','activo'),(6,'Panadería El Trigo',NULL,'5555-7777',NULL,'Zona 2','222222-2','activo'),(7,'PATITaOS S.A','Oscar Gonzalez','980374589','akl@prueba','Guatemala','0978874','activo');
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id_receta` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `id_insumo` int NOT NULL,
  `cantidad` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id_receta`),
  UNIQUE KEY `uk_producto_insumo` (`id_producto`,`id_insumo`),
  KEY `id_insumo` (`id_insumo`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `recetas_ibfk_2` FOREIGN KEY (`id_insumo`) REFERENCES `insumos` (`id_insumo`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,1,1,150.00),(2,1,2,1.00),(3,1,4,20.00),(4,1,5,20.00),(5,2,1,150.00),(6,2,2,1.00),(7,2,3,30.00);
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `descripcion` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_rol`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'administrador','Acceso total al sistema'),(2,'cocina','Visualiza y actualiza pedidos en cocina'),(3,'cajero','Gestiona ventas'),(4,'inventario','Gestiona compras e insumos');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unidades_medida`
--

DROP TABLE IF EXISTS `unidades_medida`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unidades_medida` (
  `id_unidad` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `abreviatura` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id_unidad`),
  UNIQUE KEY `nombre` (`nombre`),
  UNIQUE KEY `abreviatura` (`abreviatura`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unidades_medida`
--

LOCK TABLES `unidades_medida` WRITE;
/*!40000 ALTER TABLE `unidades_medida` DISABLE KEYS */;
INSERT INTO `unidades_medida` VALUES (1,'unidad','und'),(2,'gramo','g'),(3,'kilogramo','kg'),(4,'mililitro','ml'),(5,'litro','l');
/*!40000 ALTER TABLE `unidades_medida` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `id_rol` int NOT NULL,
  `estado` enum('activo','inactivo') COLLATE utf8mb4_unicode_ci DEFAULT 'activo',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `correo` (`correo`),
  KEY `id_rol` (`id_rol`),
  CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'admin','admin@misterburger.com','scrypt:32768:8:1$vulddniGkHbXzjNK$9edb123f3c3e320f59e05a02d627406e72b4a1f120a3e553a35507531969d6009d6a8ecf7fc73fa2260defba729b68e13ec8db7bce9f484bbca6489e23b57bc8',1,'activo','2026-03-24 13:24:42'),(2,'LCastroC','dragonboky@gmail.com','scrypt:32768:8:1$vJLp7mFW71AO4kEv$072d05180c086d04a9c5c4a93d886c4e4aed36e4f0d366ca00beb9aef323a59151248eed62d3832b65bdfbe3a59335aca465954ac9a22bfdbe18d6744c2fa4f6',3,'activo','2026-03-26 05:23:52');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta_detalle`
--

DROP TABLE IF EXISTS `venta_detalle`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta_detalle` (
  `id_venta_detalle` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `id_producto` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL,
  PRIMARY KEY (`id_venta_detalle`),
  KEY `id_venta` (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `venta_detalle_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `venta_detalle_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=66 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta_detalle`
--

LOCK TABLES `venta_detalle` WRITE;
/*!40000 ALTER TABLE `venta_detalle` DISABLE KEYS */;
INSERT INTO `venta_detalle` VALUES (1,1,1,1,25.00,25.00),(2,1,5,2,15.00,30.00),(3,2,5,1,15.00,15.00),(4,3,4,1,10.00,10.00),(5,3,1,1,25.00,25.00),(6,3,2,1,30.00,30.00),(7,3,5,1,15.00,15.00),(8,4,1,2,25.00,50.00),(9,5,1,1,25.00,25.00),(10,6,5,1,15.00,15.00),(11,7,4,1,10.00,10.00),(12,8,4,4,10.00,40.00),(13,8,1,1,25.00,25.00),(14,8,2,1,30.00,30.00),(15,9,4,1,10.00,10.00),(16,10,1,1,25.00,25.00),(17,11,1,1,25.00,25.00),(18,12,4,1,10.00,10.00),(19,12,5,1,15.00,15.00),(20,13,5,1,15.00,15.00),(21,14,5,1,15.00,15.00),(22,15,5,1,15.00,15.00),(23,16,4,1,10.00,10.00),(24,17,1,1,25.00,25.00),(25,18,4,1,10.00,10.00),(26,19,4,1,10.00,10.00),(27,20,4,1,10.00,10.00),(28,21,4,1,10.00,10.00),(29,22,1,1,25.00,25.00),(30,23,1,1,15.99,15.99),(39,32,1,1,25.00,25.00),(40,33,1,1,25.00,25.00),(41,34,1,1,25.00,25.00),(42,35,1,1,25.00,25.00),(43,36,1,1,25.00,25.00),(44,37,1,1,25.00,25.00),(45,38,1,1,25.00,25.00),(46,39,1,1,15.99,15.99),(47,40,3,1,22.99,22.99),(48,41,1,1,15.99,15.99),(49,42,1,1,15.99,15.99),(50,43,1,1,15.99,15.99),(51,44,1,1,15.99,15.99),(52,45,1,1,15.99,15.99),(53,46,1,1,15.99,15.99),(54,47,1,1,15.99,15.99),(55,48,1,1,15.99,15.99),(56,49,1,1,15.99,15.99),(57,50,1,1,15.99,15.99),(58,51,1,1,15.99,15.99),(59,52,1,1,15.99,15.99),(60,53,1,1,15.99,15.99),(61,54,1,1,15.99,15.99),(62,55,1,1,15.99,15.99),(63,56,1,1,15.99,15.99),(64,57,1,1,25.00,25.00),(65,58,1,1,25.00,25.00);
/*!40000 ALTER TABLE `venta_detalle` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `id_pedido` int DEFAULT NULL,
  `id_cliente` int DEFAULT NULL,
  `id_empleado` int NOT NULL,
  `fecha_venta` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `tipo_venta` enum('pedido_web','mostrador') COLLATE utf8mb4_unicode_ci DEFAULT 'pedido_web',
  `metodo_pago` enum('efectivo','tarjeta','transferencia','otro') COLLATE utf8mb4_unicode_ci DEFAULT 'efectivo',
  `subtotal` decimal(12,2) NOT NULL DEFAULT '0.00',
  `total` decimal(12,2) NOT NULL DEFAULT '0.00',
  `estado` enum('pagada','anulada') COLLATE utf8mb4_unicode_ci DEFAULT 'pagada',
  PRIMARY KEY (`id_venta`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_empleado` (`id_empleado`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,1,1,1,'2026-03-29 12:12:19','pedido_web','efectivo',0.00,55.00,'pagada'),(2,2,NULL,1,'2026-03-29 12:23:02','pedido_web','efectivo',15.00,15.00,'pagada'),(3,3,NULL,1,'2026-03-29 12:23:46','pedido_web','efectivo',80.00,80.00,'pagada'),(4,4,NULL,1,'2026-03-29 12:26:04','pedido_web','efectivo',50.00,50.00,'pagada'),(5,5,NULL,1,'2026-03-29 19:48:44','pedido_web','efectivo',25.00,25.00,'pagada'),(6,6,NULL,1,'2026-03-29 19:50:03','pedido_web','efectivo',15.00,15.00,'pagada'),(7,7,NULL,1,'2026-03-29 19:52:11','pedido_web','efectivo',10.00,10.00,'pagada'),(8,8,NULL,1,'2026-03-29 20:01:48','pedido_web','efectivo',95.00,95.00,'pagada'),(9,9,NULL,1,'2026-03-29 20:03:31','pedido_web','efectivo',10.00,10.00,'pagada'),(10,10,NULL,1,'2026-03-29 20:10:59','pedido_web','efectivo',25.00,25.00,'pagada'),(11,11,NULL,1,'2026-03-29 21:01:31','pedido_web','efectivo',25.00,25.00,'pagada'),(12,12,NULL,1,'2026-03-30 21:36:30','pedido_web','efectivo',25.00,25.00,'pagada'),(13,13,NULL,1,'2026-03-30 21:38:42','pedido_web','efectivo',15.00,15.00,'pagada'),(14,14,NULL,1,'2026-03-30 21:41:52','pedido_web','efectivo',15.00,15.00,'pagada'),(15,15,NULL,1,'2026-03-30 21:42:26','pedido_web','efectivo',15.00,15.00,'pagada'),(16,16,NULL,1,'2026-03-30 21:42:45','pedido_web','efectivo',10.00,10.00,'pagada'),(17,17,NULL,1,'2026-03-30 21:43:27','pedido_web','efectivo',25.00,25.00,'pagada'),(18,18,NULL,1,'2026-03-30 21:57:57','pedido_web','efectivo',10.00,10.00,'pagada'),(19,19,NULL,1,'2026-03-30 21:58:14','pedido_web','efectivo',10.00,10.00,'pagada'),(20,20,NULL,1,'2026-03-30 22:02:20','pedido_web','efectivo',10.00,10.00,'pagada'),(21,21,NULL,1,'2026-03-30 22:02:39','pedido_web','efectivo',10.00,10.00,'pagada'),(22,22,NULL,1,'2026-03-30 22:11:11','pedido_web','efectivo',25.00,25.00,'pagada'),(23,23,NULL,1,'2026-04-01 13:47:42','pedido_web','efectivo',15.99,15.99,'pagada'),(32,32,NULL,1,'2026-04-01 15:52:33','pedido_web','efectivo',25.00,25.00,'pagada'),(33,33,NULL,1,'2026-04-01 15:53:02','pedido_web','efectivo',25.00,25.00,'pagada'),(34,34,NULL,1,'2026-04-01 15:58:08','pedido_web','efectivo',25.00,25.00,'pagada'),(35,35,NULL,1,'2026-04-01 15:58:37','pedido_web','efectivo',25.00,25.00,'pagada'),(36,36,NULL,1,'2026-04-01 18:49:04','pedido_web','efectivo',25.00,25.00,'pagada'),(37,37,NULL,1,'2026-04-01 19:54:18','pedido_web','efectivo',25.00,25.00,'pagada'),(38,38,NULL,1,'2026-04-01 21:08:55','pedido_web','efectivo',25.00,25.00,'pagada'),(39,39,NULL,1,'2026-04-02 12:25:09','pedido_web','efectivo',15.99,15.99,'pagada'),(40,40,NULL,1,'2026-04-02 12:32:24','pedido_web','efectivo',22.99,22.99,'pagada'),(41,41,NULL,1,'2026-04-02 12:33:05','pedido_web','efectivo',15.99,15.99,'pagada'),(42,42,NULL,1,'2026-04-02 12:35:52','pedido_web','efectivo',15.99,15.99,'pagada'),(43,43,NULL,1,'2026-04-02 12:38:37','pedido_web','efectivo',15.99,15.99,'pagada'),(44,44,NULL,1,'2026-04-02 12:43:59','pedido_web','efectivo',15.99,15.99,'pagada'),(45,45,NULL,1,'2026-04-02 12:44:42','pedido_web','efectivo',15.99,15.99,'pagada'),(46,46,NULL,1,'2026-04-02 12:46:49','pedido_web','efectivo',15.99,15.99,'pagada'),(47,47,NULL,1,'2026-04-02 14:10:05','pedido_web','efectivo',15.99,15.99,'pagada'),(48,48,NULL,1,'2026-04-02 14:10:33','pedido_web','efectivo',15.99,15.99,'pagada'),(49,49,NULL,1,'2026-04-02 14:14:22','pedido_web','efectivo',15.99,15.99,'pagada'),(50,50,NULL,1,'2026-04-02 14:19:58','pedido_web','efectivo',15.99,15.99,'pagada'),(51,51,NULL,1,'2026-04-02 14:21:16','pedido_web','efectivo',15.99,15.99,'pagada'),(52,52,NULL,1,'2026-04-02 14:23:13','pedido_web','efectivo',15.99,15.99,'pagada'),(53,53,NULL,1,'2026-04-02 14:25:00','pedido_web','efectivo',15.99,15.99,'pagada'),(54,54,NULL,1,'2026-04-02 14:27:09','pedido_web','efectivo',15.99,15.99,'pagada'),(55,55,NULL,1,'2026-04-02 14:45:36','pedido_web','efectivo',15.99,15.99,'pagada'),(56,56,NULL,1,'2026-04-02 15:02:46','pedido_web','efectivo',15.99,15.99,'pagada'),(57,57,NULL,1,'2026-04-08 20:36:03','pedido_web','efectivo',25.00,25.00,'pagada'),(58,58,NULL,1,'2026-04-08 20:36:42','pedido_web','efectivo',25.00,25.00,'pagada');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13 21:13:39
