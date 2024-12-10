function getCSRFToken() {
    return window.csrfToken; 
  }

  const form = document.getElementById('add-business');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(form);
        console.log(formData);
        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData, 
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (!response.ok) {
              const result = await response.json();
              
              Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: Object.values(result).flat().join(', ') || 'A problem had appear',
                  confirmButtonColor: 'var(--primary-100)',
                  color: 'var(--text-100)',
                  background: 'var(--bg-100)',
              });
              return;
          }

            const result = await response.json();
            
            
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Business added to your profile',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            }).then(() => {
                location.reload();
            });

        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message || 'A problem had appear',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            });
        }
      });
      

      const formInfo = document.getElementById('modify-user');
      formInfo.addEventListener('submit', async (event) => {
        event.preventDefault();
        
        const formData = new FormData(formInfo);
        console.log(formData);
        try {
            const response = await fetch(formInfo.action, {
                method: 'POST',
                body: formData, 
                headers: {
                    'X-CSRFToken': getCSRFToken()
                }
            });

            if (!response.ok) {
              const result = await response.json();
              
              Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: Object.values(result).flat().join(', ') || 'A problem had appear',
                  confirmButtonColor: 'var(--primary-100)',
                  color: 'var(--text-100)',
                  background: 'var(--bg-100)',
              });
              return;
          }

            const result = await response.json();
            
            
            Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Data updated successfully.',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            }).then(() => {
                location.reload();
            });

        } catch (error) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: error.message || 'A problem had appear',
                confirmButtonColor: 'var(--primary-100)',
                color: 'var(--text-100)',
                background: 'var(--bg-100)',
            });
        }
      });
      