-- MySQL Script generated by MySQL Workbench
-- Tue 12 Nov 2019 09:13:15 PM -03
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema grupo2
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `grupo2` ;

-- -----------------------------------------------------
-- Schema grupo2
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `grupo2` DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci ;
USE `grupo2` ;

-- -----------------------------------------------------
-- Table `grupo2`.`tipo_instrumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`tipo_instrumento` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`tipo_instrumento` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`genero`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`genero` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`genero` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`nivel`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`nivel` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`nivel` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`preceptor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`preceptor` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`preceptor` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `apellido` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `tel` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`nucleo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`nucleo` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`nucleo` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `direccion` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `telefono` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`preceptor_nucleo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`preceptor_nucleo` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`preceptor_nucleo` (
  `preceptor_id` INT(11) NOT NULL,
  `nucleo_id` INT(11) NOT NULL,
  PRIMARY KEY (`preceptor_id`, `nucleo_id`),
  INDEX `FK_nucleo_id` (`nucleo_id` ASC),
  CONSTRAINT `FK_preceptor_id`
    FOREIGN KEY (`preceptor_id`)
    REFERENCES `grupo2`.`preceptor` (`id`),
  CONSTRAINT `FK_nucleo_id`
    FOREIGN KEY (`nucleo_id`)
    REFERENCES `grupo2`.`nucleo` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`escuela`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`escuela` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`escuela` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `direccion` VARCHAR(255) CHARACTER SET 'utf8' NULL DEFAULT NULL,
  `telefono` VARCHAR(255) CHARACTER SET 'utf8' NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`barrio`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`barrio` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`barrio` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `responsable_tipo`
--

CREATE TABLE `responsable_tipo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `responsable_tipo`
--

INSERT INTO `responsable_tipo` (`id`, `nombre`) VALUES
(1, 'Padre'),
(2, 'Madre'),
(3, 'Tutor');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `responsable_tipo`
--
ALTER TABLE `responsable_tipo`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `responsable_tipo`
--
ALTER TABLE `responsable_tipo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;


-- -----------------------------------------------------
-- Table `grupo2`.`estudiante`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`estudiante` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`estudiante` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `activo` tinyint(4) NOT NULL DEFAULT '1',
  `apellido` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `fecha_nac` DATE NOT NULL,
  `localidad_id` INT(11) NOT NULL,
  `nivel_id` INT(11) NOT NULL,
  `domicilio` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `genero_id` INT(11) NOT NULL,
  `escuela_id` INT(11) NOT NULL,
  `tipo_doc_id` INT(11) NOT NULL,
  `numero` INT(11) NOT NULL,
  `tel` VARCHAR(255) CHARACTER SET 'utf8',
  `barrio_id` INT(11) NOT NULL,
  `responsable_tipo_id` int(11) NOT NULL,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `FK_nivel_id` (`nivel_id` ASC),
  INDEX `FK_genero_estudiante_id` (`genero_id` ASC),
  INDEX `FK_escuela_id` (`escuela_id` ASC),
  INDEX `FK_barrio_id` (`barrio_id` ASC),
  CONSTRAINT `FK_nivel_id`
    FOREIGN KEY (`nivel_id`)
    REFERENCES `grupo2`.`nivel` (`id`),
  CONSTRAINT `FK_genero_estudiante_id`
    FOREIGN KEY (`genero_id`)
    REFERENCES `grupo2`.`genero` (`id`),
  CONSTRAINT `FK_escuela_id`
    FOREIGN KEY (`escuela_id`)
    REFERENCES `grupo2`.`escuela` (`id`),
  CONSTRAINT `FK_barrio_id`
    FOREIGN KEY (`barrio_id`)
    REFERENCES `grupo2`.`barrio` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`responsable`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`responsable` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`responsable` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `apellido` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `fecha_nac` DATE NOT NULL,
  `localidad_id` INT(11) NOT NULL,
  `domicilio` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `genero_id` INT(11) NOT NULL,
  `tipo_doc_id` INT(11) NOT NULL,
  `numero` INT(11) NOT NULL,
  `tel` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_genero_responsable_id` (`genero_id` ASC),
  CONSTRAINT `FK_genero_responsable_id`
    FOREIGN KEY (`genero_id`)
    REFERENCES `grupo2`.`genero` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`responsable_estudiante`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`responsable_estudiante` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`responsable_estudiante` (
  `responsable_id` INT(11) NOT NULL,
  `estudiante_id` INT(11) NOT NULL,
  PRIMARY KEY (`responsable_id`, `estudiante_id`),
  INDEX `FK_estudiante_id` (`estudiante_id` ASC),
  CONSTRAINT `FK_estudiante_id`
    FOREIGN KEY (`estudiante_id`)
    REFERENCES `grupo2`.`estudiante` (`id`),
  CONSTRAINT `FK_responsable_id`
    FOREIGN KEY (`responsable_id`)
    REFERENCES `grupo2`.`responsable` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`docente`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`docente` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`docente` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `activo` TINYINT(1) NOT NULL DEFAULT '1',
  `apellido` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `fecha_nac` DATE NOT NULL,
  `localidad_id` INT(11) NOT NULL,
  `domicilio` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `genero_id` INT(11) NOT NULL,
  `tipo_doc_id` INT(11) NOT NULL,
  `numero` INT(11) NOT NULL,
  `tel` VARCHAR(255) CHARACTER SET 'utf8',
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  INDEX `FK_genero_docente_id` (`genero_id` ASC),
  CONSTRAINT `FK_genero_docente_id`
    FOREIGN KEY (`genero_id`)
    REFERENCES `grupo2`.`genero` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`taller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`taller` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`taller` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `nombre_corto` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`ciclo_lectivo`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`ciclo_lectivo` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`ciclo_lectivo` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `fecha_ini` DATE NULL DEFAULT NULL,
  `fecha_fin` DATE NULL DEFAULT NULL,
  `semestre` TINYINT(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`docente_responsable_taller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`docente_responsable_taller` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`docente_responsable_taller` (
  `docente_id` INT(11) NOT NULL,
  `ciclo_lectivo_id` INT(11) NOT NULL,
  `taller_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `FK_docente_responsable_taller_ciclo_lectivo_id_idx` (`ciclo_lectivo_id` ASC),
  INDEX `FK_docente_responsable_taller_taller_id_idx` (`taller_id` ASC),
  CONSTRAINT `FK_docente_responsable_taller_docente_id`
    FOREIGN KEY (`docente_id`)
    REFERENCES `grupo2`.`docente` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `FK_docente_responsable_taller_ciclo_lectivo_id`
    FOREIGN KEY (`ciclo_lectivo_id`)
    REFERENCES `grupo2`.`ciclo_lectivo` (`id`),
  CONSTRAINT `FK_docente_responsable_taller_taller_id`
    FOREIGN KEY (`taller_id`)
    REFERENCES `grupo2`.`taller` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`ciclo_lectivo_taller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`ciclo_lectivo_taller` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`ciclo_lectivo_taller` (
  `taller_id` INT(11) NOT NULL,
  `ciclo_lectivo_id` INT(11) NOT NULL,
  PRIMARY KEY (`ciclo_lectivo_id`, `taller_id`),
  INDEX `FK_ciclo_lectivo_taller_taller_id` (`taller_id` ASC),
  CONSTRAINT `FK_ciclo_lectivo_taller_ciclo_lectivo_id`
    FOREIGN KEY (`ciclo_lectivo_id`)
    REFERENCES `grupo2`.`ciclo_lectivo` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `FK_ciclo_lectivo_taller_taller_id`
    FOREIGN KEY (`taller_id`)
    REFERENCES `grupo2`.`taller` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`estudiante_taller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`estudiante_taller` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`estudiante_taller` (
  `estudiante_id` INT(11) NOT NULL,
  `ciclo_lectivo_id` INT(11) NOT NULL,
  `taller_id` INT(11) NOT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`estudiante_id`, `ciclo_lectivo_id`, `taller_id`),
  INDEX `FK_estudiante_taller_ciclo_lectivo_id` (`ciclo_lectivo_id` ASC),
  INDEX `FK_estudiante_taller_taller_id` (`taller_id` ASC),
  CONSTRAINT `FK_estudiante_taller_id`
    FOREIGN KEY (`estudiante_id`)
    REFERENCES `grupo2`.`estudiante` (`id`),
  CONSTRAINT `FK_estudiante_taller_ciclo_lectivo_id`
    FOREIGN KEY (`ciclo_lectivo_id`)
    REFERENCES `grupo2`.`ciclo_lectivo` (`id`),
  CONSTRAINT `FK_estudiante_taller_taller_id`
    FOREIGN KEY (`taller_id`)
    REFERENCES `grupo2`.`taller` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`asistencia_estudiante_taller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`asistencia_estudiante_taller` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`asistencia_estudiante_taller` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `estudiante_id` INT(11) NOT NULL,
  `ciclo_lectivo_id` INT(11) NOT NULL,
  `taller_id` INT(11) NOT NULL,
  `fecha` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_asistencia_estudiante_id` (`estudiante_id` ASC),
  INDEX `FK_asistencia_ciclo_lectivo_id` (`ciclo_lectivo_id` ASC),
  INDEX `FK_asistencia_taller_id` (`taller_id` ASC),
  CONSTRAINT `FK_asistencia_estudiante_id`
    FOREIGN KEY (`estudiante_id`)
    REFERENCES `grupo2`.`estudiante` (`id`),
  CONSTRAINT `FK_asistencia_ciclo_lectivo_id`
    FOREIGN KEY (`ciclo_lectivo_id`)
    REFERENCES `grupo2`.`ciclo_lectivo` (`id`),
  CONSTRAINT `FK_asistencia_taller_id`
    FOREIGN KEY (`taller_id`)
    REFERENCES `grupo2`.`taller` (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grupo2`.`usuario`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`usuario` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`usuario` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `username` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `password` CHAR(60) CHARACTER SET 'utf8' NOT NULL,
  `activo` TINYINT(1) NOT NULL DEFAULT '1',
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `first_name` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `last_name` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`rol`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`rol` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`rol` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`permiso`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`permiso` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`permiso` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`usuario_tiene_rol`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`usuario_tiene_rol` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`usuario_tiene_rol` (
  `usuario_id` INT(11) NOT NULL,
  `rol_id` INT(11) NOT NULL,
  PRIMARY KEY (`usuario_id`, `rol_id`),
  INDEX `FK_rol_utp_id` (`rol_id` ASC),
  CONSTRAINT `FK_usuario_utp_id`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `grupo2`.`usuario` (`id`)
    ON DELETE RESTRICT
    ON UPDATE RESTRICT,
  CONSTRAINT `FK_rol_utp_id`
    FOREIGN KEY (`rol_id`)
    REFERENCES `grupo2`.`rol` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`instrumento`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`instrumento` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`instrumento` (
  `id` INT(11) NOT NULL,
  `nombre` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `tipo_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `FK_tipo_instrumento_id` (`tipo_id` ASC),
  CONSTRAINT `FK_tipo_instrumento_id`
    FOREIGN KEY (`tipo_id`)
    REFERENCES `grupo2`.`tipo_instrumento` (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_unicode_ci;


-- -----------------------------------------------------
-- Table `grupo2`.`rol_tiene_permiso`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`rol_tiene_permiso` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`rol_tiene_permiso` (
  `rol_id` INT(11) NOT NULL,
  `permiso_id` INT(11) NOT NULL,
  PRIMARY KEY (`rol_id`, `permiso_id`),
  INDEX `FK_PERMISO_ID` (`permiso_id` ASC),
  INDEX `FK_ROL_ID` (`rol_id` ASC),
  CONSTRAINT `FK_rol_id`
    FOREIGN KEY (`rol_id`)
    REFERENCES `grupo2`.`rol` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `FK_permiso_id`
    FOREIGN KEY (`permiso_id`)
    REFERENCES `grupo2`.`permiso` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `grupo2`.`config`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`config` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`config` (
  `id` INT(11) NOT NULL,
  `titulo` VARCHAR(255) NOT NULL,
  `descripcion` TEXT NOT NULL,
  `email_contacto` VARCHAR(255) NOT NULL,
  `modo_mantenimiento` TINYINT(1) NOT NULL,
  `items_por_pagina` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


--
-- Dumping data for table `config`
--

INSERT INTO `config` (`id`, `titulo`, `descripcion`, `email_contacto`, `modo_mantenimiento`, `items_por_pagina`) VALUES
(1, 'Orquesta Escuela de Berisso', 'Elegí un instrumento y escribinos a oeberisso@gmail.com o por mensaje de Facebook diciéndonos en que zona de Berisso o alrededores vivís, en que horarios vas al colegio y te informaremos en cual de nuestros núcleos podés inscribirte, o también podes acercarte los días sábados de 9 a 12 hs a la Escuela Nº 25 de Berisso, calle 126.\r\n', 'contacto@oeberisso.com.ar', 0, 2);

-- --------------------------------------------------------

--
-- Dumping data for table `permiso`
--

INSERT INTO `permiso` (`id`, `nombre`) VALUES
(1, 'usuario_index'),
(2, 'usuario_new'),
(3, 'usuario_destroy'),
(4, 'usuario_update'),
(5, 'usuario_show'),
(6, 'config_update'),
(7, 'estudiante_index'),
(8, 'estudiante_new'),
(9, 'estudiante_destroy'),
(10, 'estudiante_update'),
(11, 'estudiante_show'),
(12, 'docente_index'),
(13, 'docente_new'),
(14, 'docente_destroy'),
(15, 'docente_update'),
(16, 'docente_show'),
(17, 'ciclolectivo_index'),
(18, 'ciclolectivo_new'),
(19, 'ciclolectivo_update'),
(20, 'ciclolectivo_show'),
(21, 'taller_index'),
(22, 'taller_new'),
(23, 'taller_destroy'),
(24, 'taller_update'),
(25, 'taller_show'),
(26, 'ciclolectivo_destroy');

-- --------------------------------------------------------

--
-- Dumping data for table `rol`
--

INSERT INTO `rol` (`id`, `nombre`) VALUES
(1, 'administrador'),
(2, 'preceptor'),
(3, 'docente');

-- --------------------------------------------------------

--
-- Dumping data for table `rol_tiene_permiso`
--

INSERT INTO `rol_tiene_permiso` (`rol_id`, `permiso_id`) VALUES
(1, 1),
(1, 2),
(1, 3),
(1, 4),
(1, 5),
(1, 6),
(1, 8),
(1, 9),
(1, 12),
(1, 13),
(1, 14),
(1, 15),
(1, 16),
(1, 17),
(1, 18),
(1, 22),
(1, 26),
(2, 7),
(2, 10),
(2, 11),
(3, 7),
(3, 10),
(3, 11),
(3, 12),
(3, 16);

-- --------------------------------------------------------

INSERT INTO `genero` (`id`, `nombre`) VALUES (1, 'Masculino');
INSERT INTO `genero` (`id`, `nombre`) VALUES (2, 'Femenino');
INSERT INTO `genero` (`id`, `nombre`) VALUES (3, 'Otro');

INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES (1, 'Viento');
INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES (2, 'Cuerda');
INSERT INTO `tipo_instrumento` (`id`, `nombre`) VALUES (3, 'Percusión');

INSERT INTO `nivel` (`id`, `nombre`) VALUES (1, 'I');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (2, 'II');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (3, 'III');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (4, 'IV');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (5, 'V');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (6, 'VI');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (7, 'VII');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (8, 'VIII');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (9, 'IX');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (10, 'X');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (11, 'XI');
INSERT INTO `nivel` (`id`, `nombre`) VALUES (12, 'XII');

INSERT INTO `barrio` (`id`, `nombre`) VALUES (1, 'Barrio Náutico');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (2, 'Barrio Obrero');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (3, 'Berisso');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (4, 'Barrio Solidaridad');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (5, 'Barrio Obrero');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (6, 'Barrio Bco. Pcia.');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (7, 'Barrio J.B. Justo');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (8, 'Barrio Obrero');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (9, 'El Carmen');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (10, 'El Labrador');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (11, 'Ensenada');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (12, 'La Hermosura');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (13, 'La PLata');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (14, 'Los Talas');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (15, 'Ringuelet');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (16, 'Tolosa');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (17, 'Villa Alba');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (18, 'Villa Arguello');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (19, 'Villa B. C');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (20, 'Villa Elvira');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (21, 'Villa Nueva');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (22, 'Villa Paula');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (23, 'Villa Progreso');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (24, 'Villa San Carlos');
INSERT INTO `barrio` (`id`, `nombre`) VALUES (25, 'Villa Zula');

INSERT INTO `escuela` (`nombre`) VALUES ('502');
INSERT INTO `escuela` (`nombre`) VALUES ('Albert Thomas');
INSERT INTO `escuela` (`nombre`) VALUES ('Anexa');
INSERT INTO `escuela` (`nombre`) VALUES ('Anexo T. Speroni');
INSERT INTO `escuela` (`nombre`) VALUES ('Basiliana');
INSERT INTO `escuela` (`nombre`) VALUES ('Basiliano');
INSERT INTO `escuela` (`nombre`) VALUES ('Bellas Artes');
INSERT INTO `escuela` (`nombre`) VALUES ('Canossiano');
INSERT INTO `escuela` (`nombre`) VALUES ('Castañeda');
INSERT INTO `escuela` (`nombre`) VALUES ('Col. Nacional');
INSERT INTO `escuela` (`nombre`) VALUES ('Conquista Cristiana');
INSERT INTO `escuela` (`nombre`) VALUES ('Dardo Rocha N° 24');
INSERT INTO `escuela` (`nombre`) VALUES ('E.E.M.N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('E.M. N°26');
INSERT INTO `escuela` (`nombre`) VALUES ('E.P. Municipal N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EE N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EEE N° 501');
INSERT INTO `escuela` (`nombre`) VALUES ('EEE N°501');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N° 1');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N° 26 L.P');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N°128');
INSERT INTO `escuela` (`nombre`) VALUES ('EEM N°2');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 4');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 4 Berisso');
INSERT INTO `escuela` (`nombre`) VALUES ('EES N° 4 El Pino');
INSERT INTO `escuela` (`nombre`) VALUES ('EEST N° 1 bsso');
INSERT INTO `escuela` (`nombre`) VALUES ('EET Nº 1');
INSERT INTO `escuela` (`nombre`) VALUES ('EET Nº1');
INSERT INTO `escuela` (`nombre`) VALUES ('EGB N°25');
INSERT INTO `escuela` (`nombre`) VALUES ('EM N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EMM N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 1 L.P-');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 11');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 129');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 15');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 17');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 18');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 19');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 20');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 22');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 25');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 27');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 37 LP');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 43');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 45');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 6');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 65 La Plata');
INSERT INTO `escuela` (`nombre`) VALUES ('EP N° 7');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 15');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 19');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 20');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 24');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 25');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 45');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 55');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 6');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 65');
INSERT INTO `escuela` (`nombre`) VALUES ('EPB N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 11');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 14');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 61');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 66');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('ESB N° 9');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 10');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 13');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 19');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 2');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 20');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 22');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 23');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 24');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 25');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 27');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 3');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 43');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 45');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 501');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 6');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 66');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 7');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°11');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°17');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°19');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°3');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC N°7');
INSERT INTO `escuela` (`nombre`) VALUES ('ESC de Arte');
INSERT INTO `escuela` (`nombre`) VALUES ('ESS N° 4');
INSERT INTO `escuela` (`nombre`) VALUES ('Enseñanza Media');
INSERT INTO `escuela` (`nombre`) VALUES ('Especial N° 502');
INSERT INTO `escuela` (`nombre`) VALUES ('Estrada');
INSERT INTO `escuela` (`nombre`) VALUES ('FACULTAD');
INSERT INTO `escuela` (`nombre`) VALUES ('INDUSTRIAL');
INSERT INTO `escuela` (`nombre`) VALUES ('Italiana');
INSERT INTO `escuela` (`nombre`) VALUES ('J 904');
INSERT INTO `escuela` (`nombre`) VALUES ('J. Manuel Strada');
INSERT INTO `escuela` (`nombre`) VALUES ('Jacarandá');
INSERT INTO `escuela` (`nombre`) VALUES ('Jardín Euforion');
INSERT INTO `escuela` (`nombre`) VALUES ('Jardín N° 903');
INSERT INTO `escuela` (`nombre`) VALUES ('Jardín N° 907');
INSERT INTO `escuela` (`nombre`) VALUES ('JoaquinV.Gonzalez');
INSERT INTO `escuela` (`nombre`) VALUES ('Lola Mora sec');
INSERT INTO `escuela` (`nombre`) VALUES ('Lujan Sierra');
INSERT INTO `escuela` (`nombre`) VALUES ('MUNICIOAL 11');
INSERT INTO `escuela` (`nombre`) VALUES ('María Auxiliadora');
INSERT INTO `escuela` (`nombre`) VALUES ('María Reina');
INSERT INTO `escuela` (`nombre`) VALUES ('Media 2 España');
INSERT INTO `escuela` (`nombre`) VALUES ('Media N 1');
INSERT INTO `escuela` (`nombre`) VALUES ('Mercedita de S.Martin');
INSERT INTO `escuela` (`nombre`) VALUES ('Monseñor Alberti');
INSERT INTO `escuela` (`nombre`) VALUES ('Mtro Luis MKEY');
INSERT INTO `escuela` (`nombre`) VALUES ('Mñor. Rasore');
INSERT INTO `escuela` (`nombre`) VALUES ('N1 Francisco');
INSERT INTO `escuela` (`nombre`) VALUES ('Normal 2');
INSERT INTO `escuela` (`nombre`) VALUES ('Normal 3 LP');
INSERT INTO `escuela` (`nombre`) VALUES ('Normal n 2');
INSERT INTO `escuela` (`nombre`) VALUES ('Ntra Sra Lourdes');
INSERT INTO `escuela` (`nombre`) VALUES ('Ntra. Sra. del Valle');
INSERT INTO `escuela` (`nombre`) VALUES ('PSICOLOGIA');
INSERT INTO `escuela` (`nombre`) VALUES ('Parroquial');
INSERT INTO `escuela` (`nombre`) VALUES ('Pasos del Libertedor');
INSERT INTO `escuela` (`nombre`) VALUES ('Ped 61');
INSERT INTO `escuela` (`nombre`) VALUES ('Pedagogica');
INSERT INTO `escuela` (`nombre`) VALUES ('SEC N° 8');
INSERT INTO `escuela` (`nombre`) VALUES ('SEC N°17');
INSERT INTO `escuela` (`nombre`) VALUES ('San Simón');
INSERT INTO `escuela` (`nombre`) VALUES ('Santa Rosa');
INSERT INTO `escuela` (`nombre`) VALUES ('Sra de Fátima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Margarita');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Ro. de Lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Rosa');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta Rosa Lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta. R. de Lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Sta. Rosa de lima');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 1');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 1 Berisso');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 5');
INSERT INTO `escuela` (`nombre`) VALUES ('Técnica N° 7');
INSERT INTO `escuela` (`nombre`) VALUES ('UCALP');
INSERT INTO `escuela` (`nombre`) VALUES ('UNLP');
INSERT INTO `escuela` (`nombre`) VALUES ('UTN');
INSERT INTO `escuela` (`nombre`) VALUES ('Universitas');


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
