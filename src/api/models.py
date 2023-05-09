import os
import sys
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    rut = db.Column(db.String(20), nullable=False)
    nombre = db.Column(db.String(30), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    ciudad = db.Column(db.String(100), nullable=False)
    comuna = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    correo = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.Integer, nullable=False)
    red_social = db.Column(db.String(40), nullable=True)
    contraseña = db.Column(db.String(8), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'rut': self.rut,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'ciudad': self.ciudad,
            'comuna': self.comuna,
            'direccion': self.direccion,
            'correo': self.correo,
            'telefono': self.telefono,
            'red_social': self.red_social
        }

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'nombre': self.nombre
        }

class Servicio(db.Model):
    __tablename__ = 'servicio'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    titulo = db.Column(db.String(50))
    detalle = db.Column(db.String(500))
    precio = db.Column(db.Integer, nullable=False)
    proveedor_id = db.Column(db.Integer, ForeignKey('proveedor.id'), nullable=False)
    cobertura_servicio = db.Column(db.String(200))
    estado = db.Column(db.Boolean, default=True)
    proveedor = db.relationship('Proveedor', backref='servicios')

    def serialize(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'detalle': self.detalle,
            'precio': self.precio,
            'proveedor_id': self.proveedor_id,
            'cobertura_servicio': self.cobertura_servicio,
            'estado': self.estado,
            'proveedor': self.proveedor.serialize()
        }

class ImagenServicio(db.Model):
    __tablename__ = 'imagen_servicio'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    ruta = db.Column(db.String(400), nullable=False)
    servicio_id = db.Column(db.Integer, ForeignKey('servicio.id'), nullable=False)
    servicio = db.relationship('Servicio', backref='imagenes_servicio')

    def serialize(self):
        return {
            'id': self.id,
            'ruta': self.ruta,
            'servicio_id': self.servicio_id
        }