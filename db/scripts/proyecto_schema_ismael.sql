--
-- PostgreSQL database dump
--

\restrict cEbZsFVcB2f26kabPQ4vax55DTK0MKWq2pP80JWFLOibUOuKff462X32kg1N8d0

-- Dumped from database version 16.10
-- Dumped by pg_dump version 18.0

-- Started on 2025-11-26 22:02:14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 8 (class 2615 OID 16638)
-- Name: proyecto; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA proyecto;


--
-- TOC entry 237 (class 1259 OID 16676)
-- Name: seq_cliente_id; Type: SEQUENCE; Schema: proyecto; Owner: -
--

CREATE SEQUENCE proyecto.seq_cliente_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000000000000
    CACHE 1;


SET default_table_access_method = heap;

--
-- TOC entry 234 (class 1259 OID 16639)
-- Name: cliente; Type: TABLE; Schema: proyecto; Owner: -
--

CREATE TABLE proyecto.cliente (
    id bigint DEFAULT nextval('proyecto.seq_cliente_id'::regclass) NOT NULL,
    nombre character varying(100) NOT NULL,
    apellidos character varying(200) NOT NULL,
    fecha_nacimiento date NOT NULL,
    dni character varying(10) NOT NULL,
    email character varying(100) NOT NULL,
    nacionalidad character varying(100) NOT NULL,
    telefono bigint NOT NULL,
    direccion character varying(200) NOT NULL,
    activo boolean NOT NULL
);


--
-- TOC entry 239 (class 1259 OID 16678)
-- Name: seq_cotizacion_id; Type: SEQUENCE; Schema: proyecto; Owner: -
--

CREATE SEQUENCE proyecto.seq_cotizacion_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000000000000
    CACHE 1;


--
-- TOC entry 235 (class 1259 OID 16646)
-- Name: cotizacion; Type: TABLE; Schema: proyecto; Owner: -
--

CREATE TABLE proyecto.cotizacion (
    id bigint DEFAULT nextval('proyecto.seq_cotizacion_id'::regclass) NOT NULL,
    fecha date NOT NULL,
    precio bigint NOT NULL
);


--
-- TOC entry 238 (class 1259 OID 16677)
-- Name: seq_estado_id; Type: SEQUENCE; Schema: proyecto; Owner: -
--

CREATE SEQUENCE proyecto.seq_estado_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 10000000
    CACHE 1;


--
-- TOC entry 236 (class 1259 OID 16656)
-- Name: estado; Type: TABLE; Schema: proyecto; Owner: -
--

CREATE TABLE proyecto.estado (
    id bigint DEFAULT nextval('proyecto.seq_estado_id'::regclass) NOT NULL,
    nombre character varying(100) NOT NULL
);


--
-- TOC entry 240 (class 1259 OID 16685)
-- Name: venta; Type: TABLE; Schema: proyecto; Owner: -
--

CREATE TABLE proyecto.venta (
    id bigint NOT NULL,
    id_cliente bigint NOT NULL,
    id_precio bigint NOT NULL,
    id_estado bigint NOT NULL,
    cantidad bigint NOT NULL,
    fecha_venta date NOT NULL
);


--
-- TOC entry 241 (class 1259 OID 16706)
-- Name: seq_venta_id; Type: SEQUENCE; Schema: proyecto; Owner: -
--

CREATE SEQUENCE proyecto.seq_venta_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 100000000000000000
    CACHE 1;


--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 241
-- Name: seq_venta_id; Type: SEQUENCE OWNED BY; Schema: proyecto; Owner: -
--

ALTER SEQUENCE proyecto.seq_venta_id OWNED BY proyecto.venta.id;


--
-- TOC entry 4788 (class 2604 OID 16707)
-- Name: venta id; Type: DEFAULT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.venta ALTER COLUMN id SET DEFAULT nextval('proyecto.seq_venta_id'::regclass);


--
-- TOC entry 4790 (class 2606 OID 16643)
-- Name: cliente Cliente_pkey; Type: CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.cliente
    ADD CONSTRAINT "Cliente_pkey" PRIMARY KEY (id);


--
-- TOC entry 4794 (class 2606 OID 16660)
-- Name: estado estado_pkey; Type: CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.estado
    ADD CONSTRAINT estado_pkey PRIMARY KEY (id);


--
-- TOC entry 4792 (class 2606 OID 16650)
-- Name: cotizacion precioOro_pkey; Type: CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.cotizacion
    ADD CONSTRAINT "precioOro_pkey" PRIMARY KEY (id);


--
-- TOC entry 4796 (class 2606 OID 16689)
-- Name: venta venta_pkey; Type: CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.venta
    ADD CONSTRAINT venta_pkey PRIMARY KEY (id);


--
-- TOC entry 4797 (class 2606 OID 16690)
-- Name: venta fk_cliente_venta; Type: FK CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.venta
    ADD CONSTRAINT fk_cliente_venta FOREIGN KEY (id_cliente) REFERENCES proyecto.cliente(id);


--
-- TOC entry 4798 (class 2606 OID 16695)
-- Name: venta fk_estado_venta; Type: FK CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.venta
    ADD CONSTRAINT fk_estado_venta FOREIGN KEY (id_estado) REFERENCES proyecto.estado(id);


--
-- TOC entry 4799 (class 2606 OID 16700)
-- Name: venta fk_precio_venta; Type: FK CONSTRAINT; Schema: proyecto; Owner: -
--

ALTER TABLE ONLY proyecto.venta
    ADD CONSTRAINT fk_precio_venta FOREIGN KEY (id_precio) REFERENCES proyecto.cotizacion(id);


-- Completed on 2025-11-26 22:02:14

--
-- PostgreSQL database dump complete
--

\unrestrict cEbZsFVcB2f26kabPQ4vax55DTK0MKWq2pP80JWFLOibUOuKff462X32kg1N8d0

