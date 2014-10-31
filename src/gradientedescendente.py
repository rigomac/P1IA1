#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: t; c-basic-offset: 4; tab-width: 4 -*- 
#
# main.py
# Copyright (C) 2014 Rigo Macario <rigomacario@localhost.localdomain>
# 
# GradienteDescendente is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# GradienteDescendente is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GdkPixbuf, Gdk
import os, sys, csv,math,random


#Comment the first line and uncomment the second before installing
#or making the tarball (alternatively, use project variables)
UI_FILE = "src/gradientedescendente.ui"
#UI_FILE = "/usr/local/share/gradientedescendente/ui/gradientedescendente.ui"


class GUI:
	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file(UI_FILE)
		self.builder.connect_signals(self)

		window = self.builder.get_object('window')

		self.eArchivoX = self.builder.get_object('eArchivoX')
		self.eArchivoY = self.builder.get_object('eArchivoY')
		self.entry_m = self.builder.get_object('entry_m')
		self.entry_n = self.builder.get_object('entry_n')
		self.entry_alfa = self.builder.get_object('entry_alfa')
		self.entry_tolerancia = self.builder.get_object('entry_tolerancia')
		self.entry_iteraciones = self.builder.get_object('entry_iteraciones')

		self.bLeerArchivos = self.builder.get_object('bLeerArchivos')
		self.bCalcular = self.builder.get_object('bCalcular')
		self.entry_results = self.builder.get_object('entry_results')

		self.tmpTethas=[];

		self.store = Gtk.ListStore(int,float)
		self.treeCostos = self.builder.get_object('treeCostos')
		self.cntCosto=0

		colNum = Gtk.TreeViewColumn("NUMERO")
		title2 = Gtk.CellRendererText()
		colNum.pack_start(title2, True)
		colNum.add_attribute(title2, "text", 0)
		self.treeCostos.append_column(colNum)
		
		colCosto = Gtk.TreeViewColumn("COSTO")
		title = Gtk.CellRendererText()
		colCosto.pack_start(title, True)
		colCosto.add_attribute(title, "text", 1)
		self.treeCostos.append_column(colCosto)
		
		
		
		self.treeCostos.set_model(self.store)
		
		
		window.show_all()

	def destroy(window, self):
		Gtk.main_quit()

	#*************************************************************************** METHOD ***************

	def getVarsXFromFile(self,fileX):#obtiene todas las vars X en un arreglo
		xList=[];
		if(os.path.exists(fileX)):
			reader = csv.reader(open(fileX,'rb'))
			for index, row in enumerate(reader):
				xList.append(row);
		return xList;
	
	def getVarsYFromFile(self,fileY):#obtiene todas las vars Y en un arreglo
		yList=[];
		if(os.path.exists(fileY)):
			reader = csv.reader(open(fileY,'rb'))
			for index, row in enumerate(reader):
				yList.append(row);
		return yList;
		
	def n(self,rutaX):#obtiene el parametro "n"
		numVarsX=0;
		if(os.path.exists(rutaX)):
			reader =csv.reader(open(rutaX,'rb'))
			for index,row in enumerate(reader):
				numVarsX=len(row);			
		return numVarsX-1;
	
	def m(self,rutaX):#obtiene el parametro "m"
		lista=[];
		if(os.path.exists(rutaX)):
			reader =csv.reader(open(rutaX,'rb'))
			for index,row in enumerate(reader):
				lista.append(row)			
		return len(lista)-1;
		
		
	def derivate(self,m,n,varx,vary,tethas):
		r=0.0
		for i in range (0,m+1):#para todas las filas m
			r=r+(self.hxi(i,n,varx,vary,tethas)-self.yi(vary,i))*self.xi(varx,i,n);#
		return r;
	
	def hxi(self,m,n,varsX,varsY,tethas):
		x=varsX[m];
		y=varsY[m];
		h=0.0;
		for i in range(0,n+1):
			h=h+float(tethas[i])*float(x[i]);
		return float(h);	
		
	def costFunction(self,m,n,varx,vary,tethas):#calcula la funcion de costo
		cte=m*0.5;#1/2m
		sumat=0.0;
		for i in range (0,m+1):
			sumat=sumat+(self.hxi(i,n,varx,vary,tethas)-self.yi(vary,i));	
		sumat=sumat**2
		self.store.append([self.cntCosto,float(sumat)])
		self.cntCosto=self.cntCosto+1
		costo=float(cte*sumat)
		return costo;

	def yi(self,varsY,m):#arreglo, m Y_m, la unica columna en fila m
		varY=varsY[m];
		return float(varY[0]);
	
	def xi(self,varsX,m,n):#arreglo, m -> Retorna valor X_n^(m) o X_j^(i), x en columna n y fila m
		varX=varsX[m];
		return float(varX[n])
		
	
	def GradDesc(self,iteraciones,m,n,varx,vary,tethas,alfa,tolerancia):#m,n,varx[],vary[],tethas[],alfa,tol

		for j in range(0,n+1):#genero tethas aleatorias.
			self.tmpTethas.append(float(random.randint(1,10)));

		i=0;
		while (i<iteraciones and self.costFunction(m,n,varx,vary,self.tmpTethas)>tolerancia):
			for k in range (0,n+1):
				self.tmpTethas[k]=self.tmpTethas[k]-(alfa/m)*self.derivate(m,k,varx,vary,self.tmpTethas);
			i=i+1;		
		return self.tmpTethas;


#*************************************************************************** HANDLERS ***************
	def leerClicked(self,widget):
		rutaX=self.eArchivoX.get_text()
		rutaY=self.eArchivoY.get_text()		
		self.entry_m.set_text(str(self.m(rutaX)))
		self.entry_n.set_text(str(self.n(rutaX)))

	def calcularClicked(self,widget):
		self.tmpTethas=[];
		self.cntCosto=0
		self.store.clear()
		self.treeCostos.set_model(self.store)
		
		rutaX=self.eArchivoX.get_text()
		rutaY=self.eArchivoY.get_text()		

		iteraciones=int(self.entry_iteraciones.get_text())
		alfa=float(self.entry_alfa.get_text())
		tolerancia=float(self.entry_tolerancia.get_text())
		

		self.entry_results.set_text(str(self.GradDesc(iteraciones,self.m(rutaX),self.n(rutaX),self.getVarsXFromFile(rutaX),self.getVarsYFromFile(rutaY),self.tmpTethas,alfa,tolerancia)))

		self.treeCostos.set_model(self.store)
		
def main():
	app = GUI()
	Gtk.main()
		
if __name__ == "__main__":
	sys.exit(main())

