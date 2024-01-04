create table doctor(cedula varchar(10) default '1234567890', 
					nombre varchar(20) default 'Scarlett Valeria', 
					apellidoP varchar(15) default 'Lamas',
					apellidoM varchar(15) default 'Abbadie',
					sexo varchar(1) default 'M', 
					telefono varchar(10) default '3317746233',
					primary key(cedula)
				   );

create table paciente(nombreSC varchar(50), 
					parentesco varchar(20),
					domicilioSC varchar(30), 
					telefonoSC varchar(10),
					edad int, 
					IDpaciente serial, 
					nombre varchar(20),
					apellidoP varchar(15), 
					apellidoM varchar(15),
					sexo varchar(1), 
					domicilio varchar(30), 
					telefono varchar(10),
					correo varchar(30), 
					ocupacion varchar(15),
					residencia varchar(15), 
					origen varchar(15), 
					estado_civil varchar(15),
					cedula varchar(10),
					FOREIGN key(cedula) REFERENCES doctor(cedula) on update cascade on delete cascade,
					primary key(IDpaciente)
					);
					 
create table problemas_cronicos(
					IDpaciente serial,
					problemasCronicos varchar(30),
					primary key (IDpaciente, problemasCronicos),
					FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade
					);

create table medicamentos(
					IDpaciente serial,
					nombreM varchar(30),
					primary key (IDpaciente, nombreM),
					FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade
					);
					
create table vacunas(
					IDpaciente serial,
					tipoDeVacuna varchar(30),
					fechaVacuna date,
					primary key (IDpaciente, tipoDeVacuna),
					FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade
					);
					
create table alergias(
					IDpaciente serial,
					alergias varchar(30),
					primary key (IDpaciente, alergias),
					FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade
					);
				   
create table pagos(
					fechaP date,
					efectivo varchar(10),
					tarjeta varchar(10),
					servicio_en_linea varchar(10),
					cedula varchar(10),
					primary key(fechaP),
					FOREIGN key (cedula) REFERENCES doctor(cedula) on update cascade on delete cascade
					);
				  
create table tratamientos(
					nombreT varchar(50), 
					IDtratamiento varchar(10),
					costo varchar(10), 
					descripción varchar(100),
					medicamentos varchar(100),
					cedula varchar(10),
					primary key(IDtratamiento),
					FOREIGN key (cedula) REFERENCES doctor(cedula) on update cascade on delete cascade
					);
						 
create table realiza(
					IDpaciente serial,
					fechaP date,
					primary key(IDpaciente, fechaP),
					FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade,
					FOREIGN key (fechaP) REFERENCES pagos(fechaP) on update cascade on delete cascade
					);

create table cita(
					IDpaciente serial,
				  	cedula varchar(10),
					fechacita date,
				 	primary key(IDpaciente, cedula),
				  	FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade,
				  	FOREIGN key (cedula) REFERENCES doctor(cedula) on update cascade on delete cascade
				 	);
				 
create table tiene(
					IDpaciente serial,
				  	IDtratamiento varchar(10),
				 	primary key(IDpaciente, IDtratamiento),
				  	FOREIGN key (IDpaciente) REFERENCES paciente(IDpaciente) on update cascade on delete cascade,
				  	FOREIGN key (IDtratamiento) REFERENCES tratamientos(IDtratamiento) on update cascade on delete cascade
					);

CREATE OR REPLACE FUNCTION advertencia() RETURNS TRIGGER AS $$
BEGIN
	IF NEW.fechaCita >= CURRENT_DATE THEN
		raise exception 'Fecha de cita NO aceptada';
	END IF;
	
	IF NEW.fechaP >= CURRENT_DATE THEN
		raise exception 'Fecha NO aceptada';
	END IF;
END;
$$ language plpgsql;

CREATE TRIGGER fecha BEFORE INSERT OR UPDATE ON
cita FOR EACH ROW EXECUTE PROCEDURE advertencia();


DROP TRIGGER fecha ON cita; 



insert into doctor values(default);
insert into paciente(IDpaciente,cedula) values(2,1234567890);
insert into cita values(2,'0987654321', '14/11/22');

delete from doctor;
update doctor set cedula='0987654321' where cedula='1234567890'
delete from cita;


select idpaciente, doctor.cedula from paciente, doctor where paciente.cedula = doctor.cedula;
select * from doctor;
select * from paciente;
select * from cita;

drop table tiene;
drop table cita;
drop table problemas_cronicos;
drop table medicamentos;
drop table vacunas;
drop table alergias;
drop table realiza;
drop table pagos;
drop table tratamientos;
drop table paciente;
drop table doctor;