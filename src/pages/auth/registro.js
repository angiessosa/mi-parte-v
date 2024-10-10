import React, { useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import './registro.css';

const ImagesB = require.context('../../assets', true);

const Registro = () => {
  const [tipoDocumento, settipoDocumento] = useState('');
  const [numeroDocumento, setnumeroDocumento] = useState('');
  const [nombres, setnombres] = useState('');
  const [apellidos, setapellidos] = useState('');
  const [correoUsuario, setcorreoUsuario] = useState('');
  const [claveUsuario, setclaveUsuario] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [idRol, setidRol] = useState('');
  const [error, setError] = useState('');
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [passwordMatch, setPasswordMatch] = useState(true);

  // Estados para mostrar errores de validación
  const [numeroDocumentoError, setNumeroDocumentoError] = useState('');
  const [nombresError, setNombresError] = useState('');
  const [apellidosError, setApellidosError] = useState('');
  const [correoError, setCorreoError] = useState('');
  const [confirmPasswordError, setConfirmPasswordError] = useState('');

  // Estados para validar la contraseña
  const [isLengthValid, setIsLengthValid] = useState(false);
  const [hasUppercase, setHasUppercase] = useState(false);
  const [hasLowercase, setHasLowercase] = useState(false);
  const [hasNumber, setHasNumber] = useState(false);
  const [hasSpecialChar, setHasSpecialChar] = useState(false);

  const handlePasswordChange = (password) => {
    setclaveUsuario(password);

    // Validar si la contraseña cumple con las reglas
    setIsLengthValid(password.length >= 8);
    setHasUppercase(/[A-Z]/.test(password));
    setHasLowercase(/[a-z]/.test(password));
    setHasNumber(/\d/.test(password));
    setHasSpecialChar(/[!@#$%^&*(),.?":{}|<>]/.test(password));
  };

  const handleConfirmPasswordChange = (confirmPassword) => {
    setConfirmPassword(confirmPassword);
    setPasswordMatch(claveUsuario === confirmPassword);
  };

  const handleNumeroDocumentoChange = (value) => {
    const isValid = /^[0-9]*$/.test(value);
    setnumeroDocumento(value);
    setNumeroDocumentoError(isValid ? '' : 'El número de documento solo debe contener números');
  };

  const handleNombresChange = (value) => {
    const isValid = /^[A-Za-z\s]*$/.test(value);
    setnombres(value);
    setNombresError(isValid ? '' : 'Los nombres solo deben contener letras');
  };

  const handleApellidosChange = (value) => {
    const isValid = /^[A-Za-z\s]*$/.test(value);
    setapellidos(value);
    setApellidosError(isValid ? '' : 'Los apellidos solo deben contener letras');
  };

  const handleCorreoChange = (value) => {
    const isValid = /^[^\s@]+@[^\s@]+\.(gmail|outlook|empresa)\.com$/.test(value);
    setcorreoUsuario(value);
    setCorreoError(isValid ? '' : 'El correo debe ser válido (gmail.com, outlook.com, etc.)');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validar campos específicos
    const numeroDocumentoRegex = /^\d+$/;
    const nombresRegex = /^[A-Za-z\s]+$/;
    const correoRegex = /^[a-zA-Z0-9._%+-]+@(gmail\.com|outlook\.com|empresa\.com)$/; // Puedes agregar más dominios aquí

    if (!numeroDocumentoRegex.test(numeroDocumento)) {
      setError("El número de documento solo puede contener números.");
      return;
    }

    if (!nombresRegex.test(nombres) || !nombresRegex.test(apellidos)) {
      setError("Los nombres y apellidos solo deben contener letras.");
      return;
    }

    if (!correoRegex.test(correoUsuario)) {
      setError("El correo debe ser de un dominio permitido (gmail.com, outlook.com, empresa.com).");
      return;
    }

    // Verificar si las contraseñas coinciden
    if (claveUsuario !== confirmPassword) {
        setPasswordMatch(false);
        return;
    } else {
        setPasswordMatch(true);
    }

    // Asegurarse de que todas las reglas de la contraseña se cumplan
    if (!isLengthValid || !hasUppercase || !hasLowercase || !hasNumber || !hasSpecialChar) {
      setError("Por favor, asegúrese de que la contraseña cumpla con todas las reglas.");
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/registro', {
        tipoDocumento,
        numeroDocumento,
        nombres,
        apellidos,
        correoUsuario,
        claveUsuario,
        idRol
      });
      console.log(response.data);
      setIsSubmitted(true);
    } catch (error) {
      console.error(error.response ? error.response.data : error);
      setError("Error al registrar usuario");
    }
  };

  return (
    <div className="regisyini">
      <div>
        <nav className="navbar nnn">
          <img src={ImagesB('./logosena.png')} width="90" height="90" alt="Logo SENA" />
          <img src={ImagesB('./logobienestech.png')} alt="Logo BienesTech" />
        </nav>

        <div className="container">
          <div className="form-container">
            <h2 className="h2r">Regístrate</h2>
            <form onSubmit={handleSubmit}>
              <div className="row">
                <div className="col-md-4 mb-3">
                  <label htmlFor="document-type" className="form-label">Tipo de Documento</label>
                  <select className="tp form-selectt" value={tipoDocumento} onChange={(e) => settipoDocumento(e.target.value)} required>
                    <option value="">Seleccione una opción</option>
                    <option value="C.C">Cédula de Ciudadania</option>
                    <option value="C.E">Cédula de Extranjeria</option>
                  </select>
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="document-number" className="form-label">Número de Documento</label>
                  <input
                    type="text"
                    value={numeroDocumento}
                    className="form-controll"
                    id="document-number"
                    required
                    onChange={(e) => handleNumeroDocumentoChange(e.target.value)}
                  />
                  {numeroDocumentoError && <p className="text-danger">{numeroDocumentoError}</p>}
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="first-name" className="form-label">Nombres</label>
                  <input
                    type="text"
                    value={nombres}
                    className="form-controll"
                    id="first-name"
                    required
                    onChange={(e) => handleNombresChange(e.target.value)}
                  />
                  {nombresError && <p className="text-danger">{nombresError}</p>}
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="last-name" className="form-label">Apellidos</label>
                  <input
                    type="text"
                    value={apellidos}
                    className="form-controll"
                    id="last-name"
                    required
                    onChange={(e) => handleApellidosChange(e.target.value)}
                  />
                  {apellidosError && <p className="text-danger">{apellidosError}</p>}
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="email" className="form-label">Correo</label>
                  <input
                    type="email"
                    value={correoUsuario}
                    className="form-controll"
                    id="email"
                    required
                    onChange={(e) => handleCorreoChange(e.target.value)}
                  />
                  {correoError && <p className="text-danger">{correoError}</p>}
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="document-type" className="form-label">Rol</label>
                  <br />
                  <select className="tp form-selectt" value={idRol} onChange={(e) => setidRol(e.target.value)} required>
                    <option value="">Seleccione una opción</option>
                    <option value="1">Administrador</option>
                    <option value="2">Coordinador</option>
                  </select>
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="password" className="form-label">Contraseña</label>
                  <input
                    type="password"
                    value={claveUsuario}
                    className="form-controll"
                    id="password"
                    required
                    onChange={(e) => handlePasswordChange(e.target.value)}
                  />
                </div>
                <div className="col-md-4 mb-3">
                  <label htmlFor="confirm-password" className="form-label">Confirmar Contraseña</label>
                  <input
                    type="password"
                    value={confirmPassword}
                    className="form-controll"
                    id="confirm-password"
                    required
                    onChange={(e) => handleConfirmPasswordChange(e.target.value)}
                  />
                  {!passwordMatch && <p className="text-danger">Las contraseñas no coinciden</p>}
                </div>
              </div>

              <div className="password-rules">
                <p className={isLengthValid ? 'text-success' : 'text-danger'}>Mínimo 8 caracteres</p>
                <p className={hasUppercase ? 'text-success' : 'text-danger'}>Una letra mayúscula</p>
                <p className={hasLowercase ? 'text-success' : 'text-danger'}>Una letra minúscula</p>
                <p className={hasNumber ? 'text-success' : 'text-danger'}>Un número</p>
                <p className={hasSpecialChar ? 'text-success' : 'text-danger'}>Un carácter especial</p>
              </div>

              {error && <p className="text-danger">{error}</p>}
              <div className="submit-button-container">
                <button type="submit" className="btn btn-success">Registrarme</button>
              </div>

              {isSubmitted && (
                <div className="alert alert-success mt-3">
                  Registro exitoso
                </div>
              )}
            </form>
            <div className="text-center mt-3">
              <Link to="/login">¿Ya tienes cuenta? Inicia sesión</Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Registro;
