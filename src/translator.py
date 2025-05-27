from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator
import re
from time import sleep
from rich.console import Console

console = Console()

# Language code mappings
LANGUAGE_CODES = {
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'zh': 'chinese',
    'zh-CN': 'chinese (simplified)',
    'zh-TW': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'he': 'hebrew',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jv': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'rw': 'kinyarwanda',
    'ko': 'korean',
    'ku': 'kurdish',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar',
    'ne': 'nepali',
    'no': 'norwegian',
    'ny': 'nyanja',
    'or': 'odia',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tl': 'tagalog',
    'tg': 'tajik',
    'ta': 'tamil',
    'tt': 'tatar',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'tk': 'turkmen',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'ug': 'uyghur',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu'
}

class Translator:
    def __init__(self):
        """Initialize the translator with multiple services for better accuracy."""
        self.max_retries = 3
        self.retry_delay = 1  # seconds
        self.translation_services = ['google', 'mymemory']  # Fallback services
        self.chunk_size = 3000
        self.context_aware = True
        self.quality_mode = 'balanced'
        console.print("🌐 [green]Translation service initialized with multiple engines![/green]")
    
    def configure_quality(self, quality_mode='balanced', chunk_size=3000, context_aware=True):
        """Configure translation quality settings."""
        self.quality_mode = quality_mode
        self.context_aware = context_aware
        
        # Adjust settings based on quality mode
        if quality_mode == 'fast':
            self.chunk_size = min(chunk_size, 5000)
            self.max_retries = 2
            self.translation_services = ['google']  # Use only one service
            console.print("⚡ [yellow]Fast mode: Optimized for speed[/yellow]")
        elif quality_mode == 'high':
            self.chunk_size = min(chunk_size, 2000)
            self.max_retries = 5
            self.translation_services = ['google', 'mymemory']  # Use multiple services
            console.print("🎯 [green]High quality mode: Optimized for accuracy[/green]")
        else:  # balanced
            self.chunk_size = chunk_size
            self.max_retries = 3
            self.translation_services = ['google', 'mymemory']
            console.print("⚖️ [cyan]Balanced mode: Speed and accuracy optimized[/cyan]")
    
    def _get_language_code(self, code):
        """Convert language codes to format expected by deep_translator."""
        return LANGUAGE_CODES.get(code, code)
    
    def _smart_split_text(self, text, max_length=None):
        """Split text intelligently at sentence boundaries while preserving context."""
        if max_length is None:
            max_length = self.chunk_size
            
        if len(text) <= max_length:
            return [text]
        
        # Split by sentences first
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed the limit
            if len(current_chunk) + len(sentence) > max_length:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    # If single sentence is too long, split by clauses
                    clauses = re.split(r'(?<=[,;:])\s+', sentence)
                    for clause in clauses:
                        if len(current_chunk) + len(clause) > max_length:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = clause
                            else:
                                # If single clause is still too long, force split
                                words = clause.split()
                                temp_chunk = ""
                                for word in words:
                                    if len(temp_chunk) + len(word) > max_length:
                                        if temp_chunk:
                                            chunks.append(temp_chunk.strip())
                                            temp_chunk = word
                                        else:
                                            chunks.append(word)
                                    else:
                                        temp_chunk += " " + word if temp_chunk else word
                                if temp_chunk:
                                    current_chunk = temp_chunk
                        else:
                            current_chunk += " " + clause if current_chunk else clause
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _translate_with_service(self, text, source_lang, target_lang, service='google'):
        """Translate using a specific service."""
        try:
            source = self._get_language_code(source_lang)
            target = self._get_language_code(target_lang)
            
            if service == 'google':
                translator = GoogleTranslator(
                    source=source if source != 'auto' else 'auto',
                    target=target
                )
            elif service == 'mymemory':
                translator = MyMemoryTranslator(
                    source=source if source != 'auto' else 'auto',
                    target=target
                )
            else:
                raise Exception(f"Unknown translation service: {service}")
            
            result = translator.translate(text)
            
            if not result or result.strip() == "":
                raise Exception("Empty translation result")
            
            return result
            
        except Exception as e:
            raise Exception(f"Translation with {service} failed: {str(e)}")
    
    def _translate_chunk(self, text, source_lang=None, target_lang='en', retries=0):
        """Translate a chunk of text with multiple service fallback and retry logic."""
        for service in self.translation_services:
            try:
                console.print(f"🔄 [cyan]Translating with {service.title()}...[/cyan]")
                result = self._translate_with_service(text, source_lang, target_lang, service)
                
                # Validate translation quality
                if self._validate_translation(text, result, source_lang, target_lang):
                    return result
                else:
                    console.print(f"⚠️ [yellow]Translation quality check failed for {service}[/yellow]")
                    continue
                    
            except Exception as e:
                console.print(f"⚠️ [yellow]{service.title()} failed: {str(e)}[/yellow]")
                continue
        
        # If all services failed, retry with exponential backoff
        if retries < self.max_retries:
            console.print(f"⚠️ [yellow]All services failed, retrying... (attempt {retries + 1})[/yellow]")
            sleep(self.retry_delay * (2 ** retries))  # Exponential backoff
            return self._translate_chunk(text, source_lang, target_lang, retries + 1)
        
        raise Exception(f"Translation failed after {self.max_retries} retries with all services")
    
    def _validate_translation(self, original, translated, source_lang, target_lang):
        """Basic validation of translation quality."""
        if not translated or translated.strip() == "":
            return False
        
        # Check if translation is too similar to original (might indicate no translation occurred)
        if source_lang != target_lang and original.lower().strip() == translated.lower().strip():
            return False
        
        # Check if translation is reasonable length (not too short or too long compared to original)
        orig_len = len(original.split())
        trans_len = len(translated.split())
        
        # Allow 50% variance in word count
        if trans_len < orig_len * 0.3 or trans_len > orig_len * 3:
            return False
        
        return True
    
    def _post_process_translation(self, text, target_lang):
        """Post-process translation to improve quality."""
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Fix common punctuation issues
        text = re.sub(r'\s+([.!?,:;])', r'\1', text)
        text = re.sub(r'([.!?])\s*([A-Z])', r'\1 \2', text)
        
        # Language-specific post-processing
        if target_lang == 'fa':  # Persian/Farsi
            # Fix Persian punctuation
            text = text.replace('?', '؟')
            text = text.replace(',', '،')
        elif target_lang == 'ar':  # Arabic
            # Fix Arabic punctuation
            text = text.replace('?', '؟')
            text = text.replace(',', '،')
        
        return text
    
    def translate(self, text, source_lang='auto', target_lang='en', progress=None, task_id=None):
        """Translate text to target language with enhanced accuracy."""
        if progress and task_id:
            progress.update(task_id, advance=5, description="🔍 [yellow]Analyzing text...")
        
        # If source and target languages are the same, return original text
        if source_lang == target_lang:
            if progress and task_id:
                progress.update(task_id, advance=95)
                progress.update(task_id, description="✨ [yellow]No translation needed (same language)")
            return text
        
        try:
            # Log translation attempt
            console.print(f"\n📝 [cyan]Text length: {len(text)} characters[/cyan]")
            console.print(f"🌐 [cyan]Translating from '{source_lang}' to '{target_lang}'[/cyan]")
            console.print(f"⚙️ [cyan]Quality mode: {self.quality_mode} | Chunk size: {self.chunk_size}[/cyan]")
            
            # Smart text splitting for better context preservation
            chunks = self._smart_split_text(text, max_length=self.chunk_size)
            total_chunks = len(chunks)
            
            console.print(f"📚 [cyan]Split into {total_chunks} intelligent chunks[/cyan]")
            
            if progress and task_id:
                progress.update(task_id, advance=5, description=f"📚 [yellow]Processing {total_chunks} chunks...")
            
            translated_chunks = []
            for i, chunk in enumerate(chunks):
                if progress and task_id:
                    progress.update(
                        task_id,
                        advance=(85 / total_chunks),
                        description=f"🌍 [yellow]Translating chunk {i + 1}/{total_chunks}..."
                    )
                
                # Add context from previous chunk for better continuity (if context-aware is enabled)
                context_chunk = chunk
                if self.context_aware and i > 0 and len(translated_chunks) > 0:
                    # Add last sentence from previous translation as context
                    prev_sentences = translated_chunks[-1].split('.')
                    if len(prev_sentences) > 1:
                        context = prev_sentences[-2] + '.'
                        context_chunk = context + " " + chunk
                
                translated_chunk = self._translate_chunk(context_chunk, source_lang, target_lang)
                
                # Remove context if it was added
                if self.context_aware and i > 0 and len(translated_chunks) > 0:
                    # Try to remove the context part
                    sentences = translated_chunk.split('.')
                    if len(sentences) > 1:
                        translated_chunk = '.'.join(sentences[1:])
                
                # Post-process the translation
                translated_chunk = self._post_process_translation(translated_chunk, target_lang)
                translated_chunks.append(translated_chunk)
                
                # Brief pause to avoid rate limiting
                sleep(0.1)
            
            if progress and task_id:
                progress.update(task_id, advance=5, description="✨ [yellow]Finalizing translation...")
            
            # Join chunks and final post-processing
            final_text = ' '.join(translated_chunks)
            final_text = self._post_process_translation(final_text, target_lang)
            
            console.print(f"✨ [green]Translation completed successfully! ({len(final_text)} characters)[/green]")
            return final_text
            
        except Exception as e:
            console.print(f"❌ [red]Translation error: {str(e)}[/red]")
            raise Exception(f"Translation failed: {str(e)}") 