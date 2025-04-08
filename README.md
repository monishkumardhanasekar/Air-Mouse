<h1>Air Mouse 🖱️</h1>

<p>An AI-powered virtual mouse that tracks hand gestures using a webcam. This project uses OpenCV, MediaPipe, and Pynput to move the cursor based on finger movements and perform clicks with a simple gesture. Additionally, it supports scrolling and enhanced hand gesture recognition for a more intuitive user experience.</p>

<h2>Features</h2>
<ul>
  <li><b>Hand Tracking:</b> Uses MediaPipe to detect hand landmarks in real-time and track the movements of the fingers.</li> 
  <li><b>Cursor Control:</b> Moves the cursor based on the index finger's position relative to its starting point.</li>
  <li><b>Smooth Movement:</b> Implements a smoothing algorithm to enhance cursor precision and make movements more fluid.</li>
  <li><b>Click Detection:</b> Detects clicks when the thumb and index finger come close together (pinch gesture). </li>
  <li><b>Scroll Control:</b> Recognizes open and closed hand gestures to perform scrolling actions (up/down) on the screen.</li>
  <li><b>Adjustable Parameters:</b> Customize sensitivity, smoothing, scaling factors, and click threshold for precise control.</li>
  <li><b>Real-Time Feedback:</b> Provides visual feedback by drawing hand landmarks on the video stream.</li>
  <li><b>Multi-Hand Support:</b> Handles multiple hand gestures simultaneously for more complex interactions.</li>
</ul>

<h2>Requirements</h2>
<p>Ensure you have the following dependencies installed:</p>
<pre><code>pip install opencv-python mediapipe pynput</code></pre>

<h2>Usage</h2>
<p>Run the script to start the air mouse:</p>
<pre><code>python air_mouse.py</code></pre>

<h3>Controls</h3>
<ul>
  <li><b>Move Cursor:</b> Move your index finger to control the mouse. 👆 </li>
  <li><b>Click:</b> Pinch the thumb and index finger together. 🤏</li>
  <li><b>Scroll:</b> 
    <ul>
      <li>Open hand to scroll up. ✋ </li>
      <li>Close hand to scroll down. ✊ </li>
    </ul>
  </li>
  <li><b>Exit:</b> Press <code>q</code> to quit the application.</li>
</ul>

<h2>Configuration</h2>
<p>Modify these parameters in the script to fine-tune behavior:</p>
<ul>
  <li><code>smoothing_factor</code>: Adjusts cursor smoothing (default: <code>1.0</code>).</li>
  <li><code>scaling_factor</code>: Controls movement sensitivity (default: <code>1.0</code>).</li>
  <li><code>click_threshold</code>: Distance threshold for detecting clicks (default: <code>0.05</code>).</li>
  <li><code>screen_width</code>: Width of the screen for cursor bounds (default: <code>1920</code>).</li>
  <li><code>screen_height</code>: Height of the screen for cursor bounds (default: <code>1080</code>).</li>
  <li><code>scroll_delay</code>: Time delay between consecutive scroll actions (default: <code>0.3</code> seconds).</li>
</ul>

<h2>Limitations</h2>
<ul>
  <li>Requires a well-lit environment for accurate hand tracking and gesture recognition.</li>
  <li>Performance may vary depending on system specifications and webcam quality.</li>
  <li>Hand gestures might not be detected accurately in cluttered or low-light environments.</li>
  <li>May experience slight lag or reduced responsiveness on systems with lower processing power.</li>
</ul>

<h2>Future Enhancements</h2>
<ul>
  <li>Add right-click and other advanced mouse gestures.</li>
  <li>Improve multi-hand support for additional functionality and controls.</li>
  <li>Optimize for better performance on lower-end systems.</li>
  <li>Implement dynamic thresholding for gestures based on hand size or distance from camera.</li>
</ul>

<h2>License</h2>
<p>This project is open-source and available under the MIT License.</p>
