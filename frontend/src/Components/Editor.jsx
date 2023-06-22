import '../css/App.css';
import '../css/sb-admin-2.css'
import '../css/load.css'
import '../css/morris.css'
import '../vendor/fontawesome-free/css/all.min.css'
import React, { Fragment, useRef, useState } from 'react';
import iconImage from '../imgs/icon.png';
const apiUrl = process.env.REACT_APP_VM_IP;

function Editor({ onLogout }) {
  const [current, setCurrent] = useState(1);
  const liRef = useRef(null);
  const inputFileRef = useRef(null);
  const [textValue, setTextValue] = useState('');

  React.useLayoutEffect(() => {
    document.getElementById('defaultOpen').click();
    const liWidth = liRef.current?.offsetWidth;
    const input = document.getElementById("myfile");
    if (input && liWidth) {
      input.style.width = `${liWidth}px`;
    }
  }, []);

  const handleLogout = () => {
    onLogout();
  };

  function showTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName('tabcontent');
    for (let i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = 'none';
    }

    const tablinks = document.getElementsByClassName('tablinks');
    for (let i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(' active', '');
    }

    document.getElementById(tabName).style.display = 'block';
    evt.currentTarget.className += ' active';

    setCurrent(Array.from(tablinks).findIndex((tablink) => tablink.className.includes('active')) + 1);
  }

  function sendData() {
    // const msg = document.getElementById('TXT1');
    // setTextValue(msg.value)
    const objeto = {
      entrada: textValue,
    };

    // console.log(objeto);

    fetch(`${apiUrl}:8080/analizar`, {
      method: 'POST',
      body: JSON.stringify(objeto),
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    })
      .then((res) => res.json())
      .catch((err) => {
        console.error('Error:', err);
        alert('Something wrong happened, try again.');
      })
      .then((response) => {
        document.getElementById('console').value = response.salida;
      });
  }

  function loadFile(event) {
    setTextValue("");
    event.preventDefault(); // Prevenir el comportamiento predeterminado del formulario

    const file = inputFileRef.current.files[0];

    if (file) {
      const reader = new FileReader();
      reader.onload = function () {
        const text = reader.result;
        console.log(text)
        setTextValue(text);
        inputFileRef.current.value = '';
      };
      reader.readAsText(file);
    }
  }



  return (
    <Fragment>
      <div id="wrapper">
        <ul class="navbar-nav bg-gradient-primary sidebar sidebar-dark accordion" id="accordionSidebar">
          <div class="text-center d-none d-md-inline" style={{ paddingTop: "2.1vh" }}>
          </div>
          <hr class="sidebar-divider my-0"></hr>
          <button href="#" class="btn btn-danger btn-icon-split" onClick={handleLogout}
            style={{ width: "70%", textAlign: "center", marginRight: "auto", marginLeft: "auto", marginTop: "1rem", marginBottom: "1rem" }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-box-arrow-left" viewBox="0 0 16 16"
              style={{ marginRight: "4px", marginTop: "auto", marginBottom: "auto" }}>
              <path fill-rule="evenodd" d="M6 12.5a.5.5 0 0 0 .5.5h8a.5.5 0 0 0 .5-.5v-9a.5.5 0 0 0-.5-.5h-8a.5.5 0 0 0-.5.5v2a.5.5 0 0 1-1 0v-2A1.5 1.5 0 0 1 6.5 2h8A1.5 1.5 0 0 1 16 3.5v9a1.5 1.5 0 0 1-1.5 1.5h-8A1.5 1.5 0 0 1 5 12.5v-2a.5.5 0 0 1 1 0v2z" />
              <path fill-rule="evenodd" d="M.146 8.354a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L1.707 7.5H10.5a.5.5 0 0 1 0 1H1.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3z" />
            </svg>
            <span style={{ fontSize: "large", verticalAlign: "middle", marginLeft: "2%" }}>Log Out</span>
          </button>
          <hr class="sidebar-divider"></hr>

          <hr class="sidebar-divider my-0"></hr>
          <li class="nav-item" ref={liRef}>
            <a class="nav-link" href="#" style={{ textAlign: "center" }}>
              <div class="upload-btn-wrapper">
                <button href="#" class="btn btn-primary btn-icon-split"
                  style={{ width: "80%", textAlign: "center", marginRight: "auto", marginLeft: "auto", marginTop: "0.2rem", marginBottom: "0.2rem" }}>
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                    class="bi bi-upload" viewBox="0 0 16 16"
                    style={{ marginRight: "4px", marginTop: "auto", marginBottom: "auto" }}>
                    <path
                      d="M.5 9.9a.5.5 0 0 1 .5.5v2.5a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-2.5a.5.5 0 0 1 1 0v2.5a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2v-2.5a.5.5 0 0 1 .5-.5z" />
                    <path
                      d="M7.646 1.146a.5.5 0 0 1 .708 0l3 3a.5.5 0 0 1-.708.708L8.5 2.707V11.5a.5.5 0 0 1-1 0V2.707L5.354 4.854a.5.5 0 1 1-.708-.708l3-3z" />
                  </svg>
                  <span style={{ fontSize: "large", verticalAlign: "middle", marginleft: "2%" }}>File</span>
                </button>
                <input type="file" name="myfile" id="myfile" accept=".mia" style={{ height: "60px" }} ref={inputFileRef} />
              </div>
              <button href="#" class="btn btn-light btn-icon-split" onClick={loadFile}
              style={{width: "80%", textAlign: "center",marginRight: "auto",marginLeft: "auto",marginTop: "1rem"}}>
              <span style={{fontSize: "large",verticalAlign:"middle",marginLeft: "2%"}}>Ok</span>
            </button>
            </a>
          </li>
          <hr class="sidebar-divider"></hr>

          <hr class="sidebar-divider my-0"></hr>
          <button href="#" class="btn btn-success btn-icon-split" onClick={sendData}
            style={{ width: "80%", textAlign: "center", marginRight: "auto", marginLeft: "auto", marginTop: "1rem", marginBottom: "1rem" }}>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
              class="bi bi-play-circle-fill" viewBox="0 0 16 16"
              style={{ marginRight: "4px", marginTop: "auto", marginBottom: "auto" }}>
              <path
                d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM6.79 5.093A.5.5 0 0 0 6 5.5v5a.5.5 0 0 0 .79.407l3.5-2.5a.5.5 0 0 0 0-.814l-3.5-2.5z" />
            </svg>
            <span style={{ fontSize: "large", verticalAlign: "middle", marginLeft: "2%" }}>Run</span>
          </button>
          <hr class="sidebar-divider"></hr>
        </ul>
        <div id="content-wrapper" class="d-flex flex-column">

          <div id="content">
            <nav class="navbar navbar-expand navbar-light bg-white topbar mb-4 static-top shadow">
              <button id="sidebarToggleTop" class="btn btn-link d-md-none rounded-circle mr-3">
                <i class="fa fa-bars"></i>
              </button>
              <a href="#">
                <img src={iconImage} alt="Code" width="85" height="75" style={{marginLeft:"25px"}}></img>
              </a>

              <ul class="navbar-nav ml-auto" id="Buscar">
                <form
                  class="d-none d-sm-inline-block form-inline mr-auto ml-md-3 my-2 my-md-0 mw-100 navbar-search">
                  <div class="input-group">
                    <input type="text" class="form-control bg-light border-0 small" placeholder="Buscar..."
                      aria-label="Search" aria-describedby="basic-addon2"></input>
                    <div class="input-group-append">
                      <button class="btn btn-primary" type="submit" style={{ backgroundColor: "#00365A" }}>
                        <i class="fas fa-search fa-sm"></i>
                      </button>
                    </div>
                  </div>
                </form>

              </ul>

            </nav>



            <div class="container-fluid">
              <div class="card shadow mb-4" style={{ margin: "auto", width: "70%" }}>
                <div class="card-header py-3">
                  <h6 class="m-0 font-weight-bold text-primary">Archivo (.mia)</h6>
                </div>
                <div class="card-body" style={{ textAlign: "center", padding: "10px" }}>


                  <div class="tab" id="TabBox">
                    <button class="tablinks" onClick={(evt) => showTab(evt, 'P1')} id="defaultOpen">P1</button>
                  </div>
                  <div id="txtBox">
                    <div id="P1" class="tabcontent">
                      <textarea style={{
                        width: "100%", maxWidth: "100vh", padding: "30px", height: "50vh", textAlign: "justify", overflowX: "auto", whiteSpace: "nowrap",
                        background: "url(http://i.imgur.com/2cOaJ.png)", backgroundAttachment: "local", backgroundRepeat: "no-repeat",
                        paddingLeft: "35px", paddingTop: "10px", borderColor: "#ccc",  id: "TXT1"
                      }}
                      // defaultValue={textValue}
                      value={textValue}
                      onChange={(e) => setTextValue(e.target.value)}
                      >
                      </textarea>
                    </div>
                  </div>

                  <div class="copyright text-center my-auto">
                  </div>
                  <textarea wrap="off" id="console" readOnly style={{ width: "100%", backgroundColor: "black", color: "cyan" }} rows="10" >
                  </textarea>
                </div>
              </div>

            </div>

          </div>

          <footer class="sticky-footer bg-white">
            <div class="container my-auto">
              <div class="copyright text-center my-auto">
                <span>Copyright &copy; G14</span>
              </div>
            </div>
          </footer>

        </div>

      </div>
      <a class="scroll-to-top rounded" href="#page-top">
        <i class="fas fa-angle-up"></i>
      </a>
    </Fragment>
  );
}

export default Editor;
