"""
Contract tests for file format processing.
"""
import pytest
import tempfile
import os
from src.doc_analyzer.document_reader import DocumentReader
from src.models.document import DocumentFormat


class TestFileFormatProcessing:
    
    def setup_method(self):
        """Setup method to initialize the document reader for each test."""
        self.reader = DocumentReader()
    
    def test_md_format_processing(self):
        """Test processing of Markdown format documents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a markdown file
            md_path = os.path.join(temp_dir, "test.md")
            md_content = """# Test Document

This is a **Markdown** document.

## Features

- Feature 1
- Feature 2
- Feature 3

The system should handle *italic* and **bold** text.
            """
            
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            # Read the document
            document = self.reader.read_document(md_path)
            
            # Verify document properties
            assert document.format == DocumentFormat.MD
            assert document.title == "test"
            assert document.content == md_content
            assert document.source_path == md_path
    
    def test_html_format_processing(self):
        """Test processing of HTML format documents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create an HTML file
            html_path = os.path.join(temp_dir, "test.html")
            html_content = """<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Test HTML Document</h1>
    <p>This is an <em>HTML</em> document.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>"""
            
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Read the document
            document = self.reader.read_document(html_path)
            
            # Verify document properties
            assert document.format == DocumentFormat.HTML
            assert document.title == "test"
            assert document.content == html_content
            assert document.source_path == html_path
    
    def test_txt_format_processing(self):
        """Test processing of plain text format documents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a text file
            txt_path = os.path.join(temp_dir, "test.txt")
            txt_content = """This is a plain text document.
It contains multiple lines.
The system should read all content as is.
No formatting is applied.
            """
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(txt_content)
            
            # Read the document
            document = self.reader.read_document(txt_path)
            
            # Verify document properties
            assert document.format == DocumentFormat.TXT
            assert document.title == "test"
            assert document.content == txt_content
            assert document.source_path == txt_path
    
    def test_supported_formats_list(self):
        """Test that all supported formats are correctly listed."""
        # Check that the reader supports all expected formats
        expected_formats = {"md", "html", "pdf", "txt"}
        actual_formats = set(self.reader.supported_formats)
        
        assert expected_formats == actual_formats
    
    def test_unsupported_format_error(self):
        """Test that unsupported formats raise appropriate errors."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a file with unsupported extension
            unsupported_path = os.path.join(temp_dir, "test.xyz")
            with open(unsupported_path, 'w', encoding='utf-8') as f:
                f.write("This is an unsupported format.")
            
            # Attempt to read the document should raise an error
            with pytest.raises(ValueError) as exc_info:
                self.reader.read_document(unsupported_path)
            
            assert "Unsupported document format" in str(exc_info.value)
    
    def test_file_not_found_error(self):
        """Test that non-existent files raise appropriate errors."""
        nonexistent_path = "/path/that/does/not/exist.txt"
        
        # Attempt to read a non-existent document should raise an error
        with pytest.raises(FileNotFoundError) as exc_info:
            self.reader.read_document(nonexistent_path)
        
        assert "Document file not found" in str(exc_info.value)
    
    def test_empty_document_handling(self):
        """Test handling of empty documents."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create an empty text file
            empty_path = os.path.join(temp_dir, "empty.txt")
            with open(empty_path, 'w', encoding='utf-8') as f:
                f.write("")  # Empty file
            
            # Read the document
            document = self.reader.read_document(empty_path)
            
            # Verify document properties
            assert document.format == DocumentFormat.TXT
            assert document.title == "empty"
            assert document.content == ""
            assert document.source_path == empty_path
            
            # The document should still be valid according to our validation rules
            # (empty content is only invalid if title is also empty, which it isn't in this case)
            assert document.validate() is True