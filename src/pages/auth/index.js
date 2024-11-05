import PiePagina from '../../components/piePagina';
import React from 'react';
import { Link } from "react-router-dom";
import NavIndex from '../../components/navindex';
import '../../index.css';

const ImagesB = require.context('../../assets', true);

const Index = () => {
    return (
        <div className='index'>
                <NavIndex/>
            <div className="hold-transition index-page">
                <div className="index-box container">
                    <h2 className='h2r'>Agendar y compartir talleres de forma ágil con Bienestech</h2>
                    <div className="content-flex">
                        <div className="imgindex">
                            <img src={ImagesB('./imgindex.png')} />
                        </div>
                        <div className="text-and-buttons">
                            <div className="botones">

                                <Link to="/login">
                                    <button className="btn btn-lg btn-outline-success btn-block iniciars" type="button">Iniciar Sesión</button>
                                </Link>
                                <br></br>
                                <br></br>
                                <Link to="/registro">
                                    <button className="btn btn-lg btn-outline-success btn-block reg" type="button" Link to="./registro">Registrarse</button>
                                </Link>


                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <PiePagina />

        </div>
    );
}

export default Index;

