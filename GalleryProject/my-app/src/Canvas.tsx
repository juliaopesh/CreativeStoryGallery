import React, { useRef, useState, MouseEvent, useEffect } from 'react';

const Canvas: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);  // Ref for the canvas
  const [isDrawing, setIsDrawing] = useState<boolean>(false); // State to track drawing status

  // Initialize the canvas with a white background
  useEffect(() => {
    const canvas = canvasRef.current;
    if (canvas) {
      const ctx = canvas.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
      }
    }
  }, []);

  // Start drawing when mouse is pressed
  const handleMouseDown = () => {
    setIsDrawing(true);
  };

  // Stop drawing when mouse is released
  const handleMouseUp = () => {
    setIsDrawing(false);
    const ctx = canvasRef.current?.getContext('2d');
    ctx?.beginPath(); // Reset the drawing path if ctx is available
  };

  // Draw on the canvas as mouse moves
  const handleMouseMove = (event: MouseEvent<HTMLCanvasElement>) => {
    if (!isDrawing || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const offsetX = event.clientX - rect.left;
    const offsetY = event.clientY - rect.top;

    ctx.lineTo(offsetX, offsetY);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(offsetX, offsetY);
  };

  // Clear the canvas
  const handleClearCanvas = () => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      if (ctx) {
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);
      }
    }
  };

  // Save the canvas as JPG
  const handleSaveCanvas = () => {
    if (canvasRef.current) {
      const canvas = canvasRef.current;
      const imageUrl = canvas.toDataURL('image/jpeg', 1.0); // 1.0 for maximum quality

      const link = document.createElement('a');
      link.href = imageUrl;
      link.download = 'drawing.jpg'; // File name for the download
      link.click(); // Trigger the download by programmatically clicking the link
    } else {
      console.error('Canvas reference is null');
    }
  };

  return (
    <div>
      <h1>Creative Story Gallery</h1>
      <canvas
        ref={canvasRef}
        width={800}
        height={600}
        style={{ border: '1px solid #000', margin: '20px' }}
        onMouseDown={handleMouseDown}
        onMouseUp={handleMouseUp}
        onMouseMove={handleMouseMove}
      />
      <div>
        <button onClick={handleClearCanvas}>Clear Canvas</button>
        <button onClick={handleSaveCanvas}>Save as JPG</button>
      </div>
    </div>
  );
};

export default Canvas;