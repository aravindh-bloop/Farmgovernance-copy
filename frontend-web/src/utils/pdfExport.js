import { jsPDF } from 'jspdf';

/**
 * Download chat transcript as a formatted PDF or Text document.
 * @param {Array<{ sender: string, text: string, timestamp: string, officerRecommendation?: object }>} messages 
 * @param {string} langCode 
 * @param {string} appName 
 */
export function downloadConversationPDF(messages, langCode = 'en', appName = 'Multilingual Cooperative Assistant') {
  if (!messages || messages.length === 0) return;

  try {
    const doc = new jsPDF();
    let yPos = 20;

    // Header Title
    doc.setFontSize(18);
    doc.setTextColor(30, 64, 175); // Primary Blue
    doc.text(appName, 14, yPos);
    yPos += 8;

    doc.setFontSize(10);
    doc.setTextColor(100, 116, 139); // Slate Grey
    doc.text(`Conversation Transcript — Exported on ${new Date().toLocaleString()}`, 14, yPos);
    yPos += 6;
    doc.text(`Session Language: ${langCode.toUpperCase()}`, 14, yPos);
    yPos += 12;

    // Horizontal Divider
    doc.setDrawColor(226, 232, 240);
    doc.line(14, yPos, 196, yPos);
    yPos += 10;

    messages.forEach((msg, idx) => {
      // Check page height limit
      if (yPos > 270) {
        doc.addPage();
        yPos = 20;
      }

      const isUser = msg.sender === 'user';
      const roleText = isUser ? 'User Question:' : 'Assistant Response:';
      
      doc.setFontSize(11);
      if (isUser) {
        doc.setTextColor(16, 185, 129); // Emerald for user
      } else {
        doc.setTextColor(37, 99, 235); // Blue for assistant
      }
      doc.text(roleText, 14, yPos);
      yPos += 6;

      doc.setFontSize(10);
      doc.setTextColor(30, 41, 59); // Dark slate

      // Wrap text within margins
      const splitText = doc.splitTextToSize(msg.text, 180);
      doc.text(splitText, 14, yPos);
      yPos += (splitText.length * 5) + 4;

      // Render Officer Recommendation if present
      if (msg.officerRecommendation) {
        if (yPos > 260) {
          doc.addPage();
          yPos = 20;
        }
        doc.setFillColor(241, 245, 249);
        doc.roundedRect(14, yPos, 180, 24, 2, 2, 'F');
        
        doc.setFontSize(9);
        doc.setTextColor(15, 23, 42);
        doc.text(`Recommended Officer: ${msg.officerRecommendation.name} (${msg.officerRecommendation.designation})`, 18, yPos + 7);
        doc.text(`Office: ${msg.officerRecommendation.office}`, 18, yPos + 13);
        doc.text(`Contact / Helpline: ${msg.officerRecommendation.phone}`, 18, yPos + 19);
        yPos += 30;
      }

      yPos += 4;
    });

    doc.save(`cooperative_assistant_chat_${Date.now()}.pdf`);
  } catch (err) {
    console.warn('jsPDF export error, falling back to plain text download:', err);
    downloadAsFormattedText(messages, appName);
  }
}

function downloadAsFormattedText(messages, appName) {
  let content = `${appName}\n`;
  content += `Transcript Export — ${new Date().toLocaleString()}\n`;
  content += `=====================================================\n\n`;

  messages.forEach((msg) => {
    const isUser = msg.sender === 'user';
    content += `[${msg.timestamp || 'Time'}] ${isUser ? 'USER' : 'ASSISTANT'}:\n`;
    content += `${msg.text}\n`;
    if (msg.officerRecommendation) {
      content += `--> Recommended Officer: ${msg.officerRecommendation.name} (${msg.officerRecommendation.designation})\n`;
      content += `--> Office: ${msg.officerRecommendation.office}\n`;
      content += `--> Contact: ${msg.officerRecommendation.phone}\n`;
    }
    content += `\n-----------------------------------------------------\n\n`;
  });

  const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = `cooperative_chat_${Date.now()}.txt`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}
