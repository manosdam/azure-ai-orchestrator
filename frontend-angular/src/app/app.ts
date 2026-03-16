import { Component, signal } from '@angular/core'; // 1. Εισαγωγή signal
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent {
  model = 'LLAMA';
  userInput = '';
  chatHistory: any[] = [{ role: 'assistant', content: 'Hi! How can I assist you today?' }];
  // ΕΔΩ ΤΟ ΟΡΙΖΕΙΣ:
  streamingMsg = signal<string>('');

  loading = false;

  async handleSend() {
    if (!this.userInput.trim() || this.loading) return;

    const userMsg = { role: 'user', content: this.userInput };
    this.chatHistory.push(userMsg);
    const currentInput = this.userInput;
    this.userInput = '';
    this.loading = true;

    try {
      const response = await fetch('http://localhost:5698/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: currentInput,
          history: this.chatHistory.slice(0, -1),
          model_choice: this.model
        })
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let aiMsg = '';

      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value);
        aiMsg += chunk;

        // 3. Ενημερώνουμε το signal. Αυτό κάνει "καμπανάκι" στην Angular να κάνει refresh
        this.streamingMsg.set(aiMsg); 
      }

      this.chatHistory.push({ role: 'assistant', content: aiMsg });
      this.streamingMsg.set(''); // Καθαρισμός signal
    } catch (err) {
      this.streamingMsg.set('Error connecting to server.');
    } finally {
      this.loading = false;
    }
  }
}