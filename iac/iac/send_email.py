def send_email_presenter(event, context):

    user = event['request']['userAttributes']
    name = user['name'].split(' ')[0]
    code = event['request']['codeParameter']
    link_token = event['request'].get('linkParameter') or '{##Click Here##}'

    print(event)

    if event['triggerSource'] == 'CustomMessage_SignUp' or event['triggerSource'] == "CustomMessage_ResendCode":
        message = """
         <!DOCTYPE html>
        <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
        <!--[if gte mso 9]>
        <xml>
        <o:OfficeDocumentSettings>
        <o:AllowPNG/>
        <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml><![endif]-->

        <style type="text/css">
        @media only screen and (min-width: 620px) {{ {{
        .u-row {{ {{
        width: 600px !important;
        }}
        }}

        .u-row .u-col {{

        {{
        vertical-align: top
        ;
        }}
        }}

        .u-row .u-col-50 {{

        {{
        width: 300px !important
        ;
        }}
        }}

        .u-row .u-col-100 {{

        {{
        width: 600px !important
        ;
        }}
        }}
        }}
        }}

        @media (max-width: 620px) {{ {{
        .u-row-container {{ {{
        max-width: 100% !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        }}
        }}

        .u-row .u-col {{

        {{
        min-width: 320px !important
        ;
        max-width: 100% !important
        ;
        display: block !important
        ;
        }}
        }}

        .u-row {{

        {{
        width: 100% !important
        ;
        }}
        }}

        .u-col {{

        {{
        width: 100% !important
        ;
        }}
        }}

        .u-col > div {{

        {{
        margin: 0 auto
        ;
        }}
        }}
        }}
        }}

        body {{

        {{
        margin: 0
        ;
        padding: 0
        ;
        }}
        }}

        table, tr, td {{

        {{
        vertical-align: top
        ;
        border-collapse: collapse
        ;
        }}
        }}

        p {{

        {{
        margin: 0
        ;
        }}
        }}

        .ie-container table, .mso-container table {{

        {{
        table-layout: fixed
        ;
        }}
        }}

        * {{

        {{
        line-height: inherit
        ;
        }}
        }}

        a[x-apple-data-detectors=\'true\'] {{

        {{
        color: inherit !important
        ;
        text-decoration: none !important
        ;
        }}
        }}

        table, td {{

        {{
        color: #000000
        ;
        }}
        }}

        #u_body a {{

        {{
        color: #223166
        ;
        text-decoration: underline
        ;
        }}
        }}

        @media (max-width: 480px) {{ {{
        #u_content_heading_6 .v-container-padding-padding {{ {{
        padding: 20px 10px 40px !important;
        }}
        }}

        #u_content_heading_6 .v-font-size {{

        {{
        font-size: 20px !important
        ;
        }}
        }}

        #u_content_text_deprecated_7 .v-container-padding-padding {{

        {{
        padding: 30px 10px 10px !important
        ;
        }}
        }}

        #u_content_text_deprecated_8 .v-container-padding-padding {{

        {{
        padding: 10px 10px 30px !important
        ;
        }}
        }}

        #u_content_text_deprecated_9 .v-container-padding-padding {{

        {{
        padding: 10px 10px 20px !important
        ;
        }}
        }}
        }}
        }}
        </style>
        <title></title>
        </head>
        <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #f8f8fc;color: #000000">
        <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #f8f8fc;width:100%" cellpadding="0" cellspacing="0">
        <tbody>
        <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-50" style="max-width: 320px;min-width: 300px;display: table-cell;vertical-align: top;">
        <div style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        </div>
        </div>
        </div>
        <div class="u-col u-col-50" style="max-width: 320px;min-width: 300px;display: table-cell;vertical-align: top;">
        <div style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Open Sans',sans-serif;" align="left">
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table id="u_content_heading_6" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:25px 10px 50px;font-family:'Open Sans',sans-serif;" align="left">
        <h1 class="v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-size: 22px;"><img align="center" border="0" src="https://d2yly69bon3x8l.cloudfront.net/knowly-logo.png" alt="Logo Knowly" title="Logo Knowly" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 280px;" width="280"></h1>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table id="u_content_text_deprecated_7" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:50px 50px 0px;font-family:'Open Sans',sans-serif;" align="left">
        <div class="v-font-size" style="font-size: 15px; line-height: 140%; text-align: justify; word-wrap: break-word;">
        <p style="line-height: 140%; font-size: 14px;"><span style="font-family: 'Open Sans', sans-serif; font-size: 16px; line-height: 21px;"><strong>Olá, {name}</strong></span></p>
        <p style="line-height: 140%;">&nbsp;</p>
        <p style="line-height: 140%;">Para confirmar seu cadastro, clique no link a seguir: </p>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        <table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:15px;font-family:'Open Sans',sans-serif;" align="left">
        <div align="center">
        <a href="{link}" target="_blank" style="box-sizing: border-box;display: inline-block;font-family:'Open Sans',sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; background-color: #000000; border-radius: 4px; -webkit-border-radius: 4px; -moz-border-radius: 4px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;font-size: 14px;">
        <span style="display:block;padding:10px 20px;line-height:120%;"><strong>Verificar Email</strong></span>
        </a>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        <table id="u_content_text_deprecated_8" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:25px 10px 50px 50px;font-family:'Open Sans',sans-serif;" align="left">
        <div class="v-font-size" style="line-height: 160%; text-align: left; word-wrap: break-word;">
        <p style="font-size: 14px; line-height: 160%;">Atenciosamente,</p>
        <p style="font-size: 14px; line-height: 160%;">&nbsp;</p>
        <p style="font-size: 14px; line-height: 160%;"><strong>Equipe Knowly</strong></p>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table id="u_content_text_deprecated_9" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 100px 20px;font-family:'Open Sans',sans-serif;" align="left">
        <div class="v-font-size" style="line-height: 170%; text-align: center; word-wrap: break-word;">
        <p style="line-height: 170%;">Knowly</p>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        <table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Open Sans',sans-serif;" align="left">
        <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
        <tbody>
        <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%"><span>&nbsp;</span></td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        </body>
        </html>
        """

        # Format {name} first, then replace {link} with Cognito's placeholder
        message = message.format(name=name, link=link_token)

        event["response"]["emailMessage"] = message
        event["response"]["emailSubject"] = 'Confirme seu cadastro - Knowly'

    if event['triggerSource'] == 'CustomMessage_ForgotPassword':

        message = """
         <!DOCTYPE html>
        <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
        <head>
        <!--[if gte mso 9]>
        <xml>
        <o:OfficeDocumentSettings>
        <o:AllowPNG/>
        <o:PixelsPerInch>96</o:PixelsPerInch>
        </o:OfficeDocumentSettings>
        </xml><![endif]-->

        <style type="text/css">
        @media only screen and (min-width: 620px) {{ {{
        .u-row {{ {{
        width: 600px !important;
        }}
        }}

        .u-row .u-col {{

        {{
        vertical-align: top
        ;
        }}
        }}

        .u-row .u-col-50 {{

        {{
        width: 300px !important
        ;
        }}
        }}

        .u-row .u-col-100 {{

        {{
        width: 600px !important
        ;
        }}
        }}
        }}
        }}

        @media (max-width: 620px) {{ {{
        .u-row-container {{ {{
        max-width: 100% !important;
        padding-left: 0px !important;
        padding-right: 0px !important;
        }}
        }}

        .u-row .u-col {{

        {{
        min-width: 320px !important
        ;
        max-width: 100% !important
        ;
        display: block !important
        ;
        }}
        }}

        .u-row {{

        {{
        width: 100% !important
        ;
        }}
        }}

        .u-col {{

        {{
        width: 100% !important
        ;
        }}
        }}

        .u-col > div {{

        {{
        margin: 0 auto
        ;
        }}
        }}
        }}
        }}

        body {{

        {{
        margin: 0
        ;
        padding: 0
        ;
        }}
        }}

        table, tr, td {{

        {{
        vertical-align: top
        ;
        border-collapse: collapse
        ;
        }}
        }}

        p {{

        {{
        margin: 0
        ;
        }}
        }}

        .ie-container table, .mso-container table {{

        {{
        table-layout: fixed
        ;
        }}
        }}

        * {{

        {{
        line-height: inherit
        ;
        }}
        }}

        a[x-apple-data-detectors=\'true\'] {{

        {{
        color: inherit !important
        ;
        text-decoration: none !important
        ;
        }}
        }}

        table, td {{

        {{
        color: #000000
        ;
        }}
        }}

        #u_body a {{

        {{
        color: #223166
        ;
        text-decoration: underline
        ;
        }}
        }}

        @media (max-width: 480px) {{ {{
        #u_content_heading_6 .v-container-padding-padding {{ {{
        padding: 20px 10px 40px !important;
        }}
        }}

        #u_content_heading_6 .v-font-size {{

        {{
        font-size: 20px !important
        ;
        }}
        }}

        #u_content_text_deprecated_7 .v-container-padding-padding {{

        {{
        padding: 30px 10px 10px !important
        ;
        }}
        }}

        #u_content_text_deprecated_8 .v-container-padding-padding {{

        {{
        padding: 10px 10px 30px !important
        ;
        }}
        }}

        #u_content_text_deprecated_9 .v-container-padding-padding {{

        {{
        padding: 10px 10px 20px !important
        ;
        }}
        }}
        }}
        }}
        </style>
        <title></title>
        </head>
        <body class="clean-body u_body" style="margin: 0;padding: 0;-webkit-text-size-adjust: 100%;background-color: #f8f8fc;color: #000000">
        <table id="u_body" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;min-width: 320px;Margin: 0 auto;background-color: #f8f8fc;width:100%" cellpadding="0" cellspacing="0">
        <tbody>
        <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top">
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-50" style="max-width: 320px;min-width: 300px;display: table-cell;vertical-align: top;">
        <div style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        </div>
        </div>
        </div>
        <div class="u-col u-col-50" style="max-width: 320px;min-width: 300px;display: table-cell;vertical-align: top;">
        <div style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px;font-family:'Open Sans',sans-serif;" align="left">
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="background-color: #000000;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table id="u_content_heading_6" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:25px 10px 50px;font-family:'Open Sans',sans-serif;" align="left">
        <h1 class="v-font-size" style="margin: 0px; color: #ffffff; line-height: 140%; text-align: center; word-wrap: break-word; font-size: 22px;"><img align="center" border="0" src="https://d2yly69bon3x8l.cloudfront.net/knowly-logo.png" alt="Logo Knowly" title="Logo Knowly" style="outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;clear: both;display: inline-block !important;border: none;height: auto;float: none;width: 100%;max-width: 280px;" width="280"></h1>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="background-color: #ffffff;height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table id="u_content_text_deprecated_7" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:50px 50px 0px;font-family:'Open Sans',sans-serif;" align="left">
        <div class="v-font-size" style="font-size: 15px; line-height: 140%; text-align: justify; word-wrap: break-word;">
        <p style="line-height: 140%; font-size: 14px;"><span style="font-family: 'Open Sans', sans-serif; font-size: 16px; line-height: 21px;"><strong>Olá, {name}</strong></span></p>
        <p style="line-height: 140%;">&nbsp;</p>
        <p style="line-height: 140%;">Para confirmar seu cadastro, clique no link a seguir: </p>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        <table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:15px;font-family:'Open Sans',sans-serif;" align="left">
        <div align="center">
        <a href="{link}" target="_blank" style="box-sizing: border-box;display: inline-block;font-family:'Open Sans',sans-serif;text-decoration: none;-webkit-text-size-adjust: none;text-align: center;color: #FFFFFF; background-color: #000000; border-radius: 4px; -webkit-border-radius: 4px; -moz-border-radius: 4px; width:auto; max-width:100%; overflow-wrap: break-word; word-break: break-word; word-wrap:break-word; mso-border-alt: none;font-size: 14px;">
        <span style="display:block;padding:10px 20px;line-height:120%;"><strong>Verificar Email</strong></span>
        </a>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        <table id="u_content_text_deprecated_8" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:25px 10px 50px 50px;font-family:'Open Sans',sans-serif;" align="left">
        <div class="v-font-size" style="line-height: 160%; text-align: left; word-wrap: break-word;">
        <p style="font-size: 14px; line-height: 160%;">Atenciosamente,</p>
        <p style="font-size: 14px; line-height: 160%;">&nbsp;</p>
        <p style="font-size: 14px; line-height: 160%;"><strong>Equipe Knowly</strong></p>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        <div class="u-row-container" style="padding: 0px;background-color: transparent">
        <div class="u-row" style="Margin: 0 auto;min-width: 320px;max-width: 600px;overflow-wrap: break-word;word-wrap: break-word;word-break: break-word;background-color: transparent;">
        <div style="border-collapse: collapse;display: table;width: 100%;height: 100%;background-color: transparent;">
        <div class="u-col u-col-100" style="max-width: 320px;min-width: 600px;display: table-cell;vertical-align: top;">
        <div style="height: 100%;width: 100% !important;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <div style="box-sizing: border-box; height: 100%; padding: 0px;border-top: 0px solid transparent;border-left: 0px solid transparent;border-right: 0px solid transparent;border-bottom: 0px solid transparent;border-radius: 0px;-webkit-border-radius: 0px; -moz-border-radius: 0px;">
        <table id="u_content_text_deprecated_9" style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:10px 100px 20px;font-family:'Open Sans',sans-serif;" align="left">
        <div class="v-font-size" style="line-height: 170%; text-align: center; word-wrap: break-word;">
        <p style="line-height: 170%;">Knowly</p>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        <table style="font-family:'Open Sans',sans-serif;" role="presentation" cellpadding="0" cellspacing="0" width="100%" border="0">
        <tbody>
        <tr>
        <td class="v-container-padding-padding" style="overflow-wrap:break-word;word-break:break-word;padding:0px;font-family:'Open Sans',sans-serif;" align="left">
        <table height="0px" align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;table-layout: fixed;border-spacing: 0;mso-table-lspace: 0pt;mso-table-rspace: 0pt;vertical-align: top;border-top: 1px solid #BBBBBB;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%">
        <tbody>
        <tr style="vertical-align: top">
        <td style="word-break: break-word;border-collapse: collapse !important;vertical-align: top;font-size: 0px;line-height: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%"><span>&nbsp;</span></td>
        </tr>
        </tbody>
        </table>
        </td>
        </tr>
        </tbody>
        </table>
        </div>
        </div>
        </div>
        </div>
        </div>
        </div>
        </td>
        </tr>
        </tbody>
        </table>
        </body>
        </html>
        """

        # Format {name} and {link} together
        message = message.format(name=name, link='{##Reset Password##}')

        event["response"]["emailMessage"] = message
        event["response"]["emailSubject"] = 'Criar nova senha - Knowly'

    print(event)

    return event

def lambda_handler(event, context):
    response = send_email_presenter(event, context)

    return response