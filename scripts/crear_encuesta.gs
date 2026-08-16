/**
 * Lima Automa - Generador de Encuesta de Validación
 * =================================================
 * Copia este script en Google Apps Script y ejecútalo
 * para crear la encuesta automáticamente en Google Forms.
 */

function crearEncuesta() {
  // Crear nueva encuesta
  var form = FormApp.create('Encuesta Lima Automa - Validación de Negocio');
  
  // Configurar descripción
  form.setDescription('Encuesta para restaurantes en Lima. Tu opinión nos ayuda a crear un servicio que realmente necesites.');
  form.setIsAcceptingResponses(true);
  
  // ============ SECCIÓN 1: SOBRE TU RESTAURANTE ============
  var section1 = form.addSectionHeaderItem();
  section1.setTitle('Sobre tu Restaurante');
  section1.setHelpText('Cuéntanos sobre tu negocio');
  
  // Pregunta 1: Tipo de restaurante
  form.addMultipleChoiceItem()
    .setTitle('¿Qué tipo de restaurante tienes?')
    .setChoiceValues(['Cevichería', 'Pollería', 'Pizzería', 'Café/Cafetería', 'Restaurante general', 'Comida rápida', 'Otro'])
    .isRequired(true);
  
  // Pregunta 2: Distrito
  form.addMultipleChoiceItem()
    .setTitle('¿En qué distrito está tu restaurante?')
    .setChoiceValues(['Miraflores', 'San Isidro', 'Barranco', 'Santiago de Surco', 'San Borja', 'Jesús María', 'La Molina', 'San Martín de Porres', 'Otro'])
    .isRequired(true);
  
  // Pregunta 3: Clientes diarios
  form.addMultipleChoiceItem()
    .setTitle('¿Cuántos clientes atiendes al día aproximadamente?')
    .setChoiceValues(['0-20 clientes', '21-50 clientes', '51-100 clientes', 'Más de 100 clientes'])
    .isRequired(true);
  
  // ============ SECCIÓN 2: NECESIDADES ============
  var section2 = form.addSectionHeaderItem();
  section2.setTitle('Tus Necesidades');
  section2.setHelpText('Cuéntanos qué necesitas para crecer');
  
  // Pregunta 4: Clientes nuevos necesarios
  form.addMultipleChoiceItem()
    .setTitle('¿Cuántos clientes NUEVOS necesitas al mes?')
    .setChoiceValues(['0-10 clientes nuevos', '11-30 clientes nuevos', '31-50 clientes nuevos', 'Más de 50 clientes nuevos'])
    .isRequired(true);
  
  // Pregunta 5: Mayor problema
  form.addMultipleChoiceItem()
    .setTitle('¿Cuál es tu mayor problema actualmente?')
    .setChoiceValues(['No tengo suficientes clientes', 'No tengo tiempo para marketing', 'No sé cómo hacer marketing digital', 'No tengo presupuesto para marketing', 'La competencia es muy fuerte'])
    .isRequired(true);
  
  // Pregunta 6: Gasto en marketing
  form.addMultipleChoiceItem()
    .setTitle('¿Cuánto pagas actualmente por marketing o publicidad?')
    .setChoiceValues(['Nada, no invierto en marketing', 'S/ 0 - 500 al mes', 'S/ 500 - 1,000 al mes', 'S/ 1,000 - 2,000 al mes', 'Más de S/ 2,000 al mes'])
    .isRequired(true);
  
  // ============ SECCIÓN 3: SOLUCIÓN ============
  var section3 = form.addSectionHeaderItem();
  section3.setTitle('Nuestra Propuesta');
  section3.setHelpText('Imagina un servicio que te traiga clientes directamente');
  
  // Pregunta 7: Interés en modelo de comisión
  form.addMultipleChoiceItem()
    .setTitle('¿Te gustaría pagar SOLO por cada cliente nuevo que te traemos? (Sin costo fijo mensual)')
    .setChoiceValues(['Sí, me interesa mucho', 'Sí, pero tengo dudas', 'Prefiero pagar una mensualidad fija', 'No me interesa'])
    .isRequired(true);
  
  // Pregunta 8: Disposición a pagar
  form.addMultipleChoiceItem()
    .setTitle('¿Cuánto estarías dispuesto a pagar por cada cliente nuevo que te traemos?')
    .setChoiceValues(['S/ 5 por cliente', 'S/ 10 por cliente', 'S/ 15 por cliente', 'S/ 20 por cliente', 'S/ 25 por cliente', 'S/ 30 por cliente'])
    .isRequired(true);
  
  // Pregunta 9: Servicio más interesante
  form.addMultipleChoiceItem()
    .setTitle('¿Qué servicio te interesa más?')
    .setChoiceValues(['Traer clientes nuevos a mi restaurante', 'Automatizar pedidos por WhatsApp', 'Ambos servicios juntos', 'Ninguno me interesa'])
    .isRequired(true);
  
  // Pregunta 10: Mes gratis
  form.addMultipleChoiceItem()
    .setTitle('¿Te gustaría probar 1 mes gratis sin compromiso?')
    .setChoiceValues(['Sí, obvio que sí', 'Tal vez, necesito más información', 'No, gracias'])
    .isRequired(true);
  
  // ============ SECCIÓN 4: CONTACTO ============
  var section4 = form.addSectionHeaderItem();
  section4.setTitle('Contacto (Opcional)');
  section4.setHelpText('Si quieres que te contactemos, déjanos tus datos');
  
  // Pregunta 11: Nombre
  form.addTextItem()
    .setTitle('¿Cuál es tu nombre?')
    .setHelpText('Opcional')
    .setRequired(false);
  
  // Pregunta 12: WhatsApp
  form.addTextItem()
    .setTitle('¿Cuál es tu número de WhatsApp?')
    .setHelpText('Opcional - Te contactaremos para ofrecerte el servicio gratis')
    .setRequired(false);
  
  // Pregunta 13: Email
  form.addTextItem()
    .setTitle('¿Cuál es tu correo electrónico?')
    .setHelpText('Opcional')
    .setRequired(false);
  
  // ============ CONFIGURACIÓN FINAL ============
  form.setAllowResponseEdits(false);
  form.setCollectEmail(false);
  form.setShowLinkToRespondAgain(false);
  
  // Guardar ID del formulario
  var formId = form.getId();
  var formUrl = form.getPublishedUrl();
  var editUrl = form.getEditUrl();
  
  Logger.log('========================================');
  Logger.log('ENCUESTA CREADA EXITOSAMENTE');
  Logger.log('========================================');
  Logger.log('ID del formulario: ' + formId);
  Logger.log('URL para compartir: ' + formUrl);
  Logger.log('URL para editar: ' + editUrl);
  Logger.log('========================================');
  
  // Mostrar URL en la consola
  Logger.log('\nCOMPARTE ESTA URL CON LOS RESTAURANTES:');
  Logger.log(formUrl);
  
  return formUrl;
}

/**
 * Esta función se ejecuta automáticamente al abrir el script
 */
function onOpen() {
  var ui = FormApp.getUi();
  ui.createMenu('Lima Automa')
    .addItem('Crear Encuesta', 'crearEncuesta')
    .addToUi();
}
