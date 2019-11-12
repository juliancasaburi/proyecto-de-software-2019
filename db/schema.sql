-- MySQL Script generated by MySQL Workbench
-- Tue 12 Nov 2019 07:02:35 PM -03
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


-- -----------------------------------------------------
-- Table `grupo2`.`estudiante`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `grupo2`.`estudiante` ;

CREATE TABLE IF NOT EXISTS `grupo2`.`estudiante` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
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
  `tel` VARCHAR(255) CHARACTER SET 'utf8' NOT NULL,
  `barrio_id` INT(11) NOT NULL,
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
  `fecha_ini` DATETIME NULL DEFAULT NULL,
  `fecha_fin` DATETIME NULL DEFAULT NULL,
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
    REFERENCES `grupo2`.`taller` (`id`))
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
  `activo` TINYINT(1) NOT NULL DEFAULT '0',
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
  INDEX `FK_PERMISO_ID` (`permiso_id` ASC),
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


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
