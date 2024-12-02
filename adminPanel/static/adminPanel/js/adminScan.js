//SCAN QR
const startScanButton = document.getElementById('turn-cam');
const readerDiv = document.getElementById('reader');
let html5QrCode;
let scanning = false;

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
                        checkCode(qrCodeMessage);
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
                const response = await fetch(`/adminpanel/check-code-api/?code=${encodeURIComponent(code)}`, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()  
                    }
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
                });
          
            } catch (error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: error.message,
                });
            }
          }