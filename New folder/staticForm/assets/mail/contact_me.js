$(function () {
    $(
        "#contactForm input,#contactForm textarea,#contactForm button"
    ).jqBootstrapValidation({
        preventSubmit: true,
        submitError: function ($form, event, errors) {
            // additional error messages or events
            debugger
        },
        submitSuccess: function ($form, event) {
            event.preventDefault(); // prevent default submit behaviour
            // get values from FORM
            var name = $("input#name").val();
            var email = $("input#email").val();
            var phone = $("input#phone").val();
            var message = $("textarea#message").val();
            var firstName = name; // For Success/Failure Message
            // Check for white space in name for Success/Fail message
            if (firstName.indexOf(" ") >= 0) {
                firstName = name.split(" ").slice(0, -1).join(" ");
            }
            $this = $("#sendMessageButton");
            $this.prop("disabled", true); // Disable submit button until AJAX call is complete to prevent duplicate messages
            Email.send({
                Host : "smtp.mailtrap.io",
                Username : "7bdda96fcccef1",
                Password : "fa0e86d91b1d97",
                To : 'huyp26102000@gmail.com',
                From : "sender@example.com",
                Subject : "Contact Message",
                Body : `<html > <head>
                <style>
                table {
                  font-family: arial, sans-serif;
                  border-collapse: collapse;
                  width: 100%;
                }
                
                td, th {
                  border: 1px solid #dddddd;
                  text-align: left;
                  padding: 8px;
                }
                
                tr:nth-child(even) {
                  background-color: #dddddd;
                }
                </style>
                </head><table>
                <tr>
                  <th>Customer Name</th>
                  <th>Customer Email</th>
                  <th>Customer Phone</th>
                  <th>Customer Message</th>
                </tr>
                <tr>
                  <td>${name}</td>
                  <td>${email}</td>
                  <td>${phone}</td>
                  <td>${message}</td>
                </tr>
              
              </table></html>`
            }).then(
              message => {
                Swal.fire({
                    position: 'center',
                    icon: 'success',
                    title: 'Thanks for your contact!',
                    showConfirmButton: false,
                    timer: 1500
                  })
            }
            );
        },
        filter: function () {
            return $(this).is(":visible");
        },
    });

    $('a[data-toggle="tab"]').click(function (e) {
        e.preventDefault();
        $(this).tab("show");
    });
});

/*When clicking on Full hide fail/success boxes */
$("#name").focus(function () {
    $("#success").html("");
});
