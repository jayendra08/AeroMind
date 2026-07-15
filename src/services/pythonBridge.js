const path = require('path');
const { spawn } = require('child_process');

function runPythonPrediction(payload) {
  return new Promise((resolve, reject) => {
    const pythonExecutable = process.env.PYTHON_EXECUTABLE || 'python';
    const scriptPath = path.resolve(__dirname, '../../../ml/predict_micro_location.py');
    const child = spawn(pythonExecutable, [scriptPath], {
      cwd: path.resolve(__dirname, '../../../ml'),
      env: {
        ...process.env,
        PYTHONUNBUFFERED: '1',
      },
      windowsHide: true,
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (chunk) => {
      stdout += chunk.toString();
    });

    child.stderr.on('data', (chunk) => {
      stderr += chunk.toString();
    });

    child.on('error', (error) => {
      reject(error);
    });

    child.on('close', (code) => {
      if (code !== 0) {
        return reject(new Error(stderr || `Python prediction exited with code ${code}`));
      }

      try {
        const parsed = JSON.parse(stdout.trim());
        if (parsed.error) {
          return reject(new Error(parsed.error));
        }
        resolve(parsed);
      } catch (error) {
        reject(new Error(`Unable to parse Python output: ${error.message}\n${stdout}\n${stderr}`));
      }
    });

    child.stdin.write(JSON.stringify(payload));
    child.stdin.end();
  });
}

module.exports = { runPythonPrediction };
