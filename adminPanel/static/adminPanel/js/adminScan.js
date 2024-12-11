//SCAN QR
const startScanButton = document.getElementById('turn-cam');
const readerDiv = document.getElementById('reader');
let html5QrCode;
let scanning = false;
let reedem = false;


function changeReedem(){
  reedem = !reedem;
  if (reedem == true) {
      var modal = document.getElementById("add-form-scan");
      modal.style.display = "none";
      var modal = document.getElementById("reedem-scan");
      modal.style.display = "flex";
      document.getElementById("change-reedem").textContent = 'Change to add';
  }else{
    var modal = document.getElementById("reedem-scan");
      modal.style.display = "none";
      document.getElementById("change-reedem").textContent = 'Change to reedem';
      var modal = document.getElementById("add-form-scan");
      modal.style.display = "flex";
  }
}

        async function scanAction(id){
          if (scanning || id !== null) {
              html5QrCode.stop().then(ignore => {
                scanning = false;
                if (id !==null ){
                  scanActionDo(id);
                }else{
                  startScanButton.textContent = 'Turn On';
                }
            }).catch(err => {
                console.log(`Something wrong happend stoping the scan: ${err}`);
            });
            
        } else {
          scanActionDo(null)
        }
        function scanActionDo(id){
          Html5Qrcode.getCameras().then(cameras => {
            if (cameras && cameras.length) {
                if (id == null){
                  var cameraId = cameras[0].id;
                }else{
                  var cameraId = id;
                }
                
                const cameraList = document.getElementById('choose-cam');
                cameraList.innerHTML = '';
                cameras.forEach((camera, index) => {
                  const li = document.createElement('li');
                  li.textContent = camera.label || `Cámara ${index + 1}`;
                  li.setAttribute('data-camera-id', camera.id);
                  li.onclick = () => scanAction(camera.id)
                  cameraList.appendChild(li);
                });
                html5QrCode = new Html5Qrcode("reader");
                readerDiv.style.display = 'block';

                html5QrCode.start(
                    cameraId, 
                    {
                        fps: 10,    
                        qrbox: 250  
                    },
                    qrCodeMessage => {

                      if (reedem == true){
                        checkCode(qrCodeMessage);
                      } else {
                        addPoints(qrCodeMessage);
                      }  
                        scanAction(null);
                    },
                    errorMessage => {
                      
                    })
                    .then(() => {
                        scanning = true;
                        startScanButton.textContent = 'Turn Off';
                    })
                    .catch(err => {
                      Swal.fire({
                        icon: "error",
                        title: "Something wrong happend starting the camera",
                        text: err,
                        confirmButtonColor: 'var(--primary-100)',
                        color: 'var(--text-100)',
                        background: 'var(--bg-100)',
                      });
                    });
            }
        }).catch(err => {
          Swal.fire({
            icon: "error",
            title: "Something wrong happend getting the cameras list",
            text: err,
            confirmButtonColor: 'var(--primary-100)',
            color: 'var(--text-100)',
            background: 'var(--bg-100)',
          });
        });
        }
        }


        async function checkCode(code) {
            try {
                const username = document.querySelector('#username').value; 
                if (!username) {
                  Swal.fire({
                      icon: 'error',
                      title: 'Validation Error',
                      text: 'Username is required.',
                      confirmButtonColor: 'var(--primary-100)',
                      background: 'var(--bg-100)',
                      color: 'var(--text-100)'
                  });
                  return;
                }
                const requestData = {
                  code: code,
                  username: username
              };

                const response = await fetch(`/administration/check-code-api/`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()  
                    },
                    body: JSON.stringify(requestData)
                });
          
                if (!response.ok) {
                    const errorData = await response.json();
                    Swal.fire({
                      icon: 'error',
                      title: 'Error',
                      confirmButtonColor: 'var(--primary-100)',
                      background: 'var(--bg-100)',
                      color: 'var(--text-100)',
                      text: errorData.error || 'Something wrong in the code verification.',
                    });
                    return;
                }
          
                Swal.fire({
                  title: 'Success',
                  text: 'The gift was successfully claimed.',
                  icon: 'success',
                  showConfirmButton: true, 
                  background: 'var(--bg-100)',
                }).then(() => {
                  window.location.reload(); 
              });
          
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            }
          }


          async function addPoints(code) {
            try {
              const amount = document.querySelector('#amount').value; 
              const business = document.querySelector('#business').value;
              
              if (!amount || !business) {
                Swal.fire({
                    icon: 'error',
                    title: 'Validation Error',
                    text: 'Both amount and business are required.',
                    confirmButtonColor: 'var(--primary-100)',
                    background: 'var(--bg-100)',
                    color: 'var(--text-100)'
                });
                return;
            }
              const requestData = {
                code: code,
                amount: amount,
                business: business
            };
                const response = await fetch(`/administration/check-code-api/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()  
                    },
                    body: JSON.stringify(requestData)
                });
          
                if (!response.ok) {
                    const errorData = await response.json();
                    Swal.fire({
                      icon: 'error',
                      title: 'Error',
                      confirmButtonColor: 'var(--primary-100)',
                      background: 'var(--bg-100)',
                      color: 'var(--text-100)',
                      text: errorData.error || 'Something wrong in the process.',
                    });
                    return;
                }
          
                Swal.fire({
                  title: 'Success',
                  text: 'The points have been sent.',
                  icon: 'success',
                  showConfirmButton: true, 
                  background: 'var(--bg-100)',
                }).then(() => {
                  window.location.reload(); 
              });
          
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            }
          }