# Install Without Rust - Using Pre-built Wheels

## Run these commands in PowerShell:

```powershell
# Step 1: Upgrade pip and install wheel tools
python.exe -m pip install --upgrade pip wheel setuptools

# Step 2: Install packages using pre-built binary wheels only
# This avoids compiling from source (which requires Rust)
pip install --only-binary :all: -r requirements.txt

# If Step 2 fails, try installing problematic packages individually:
pip install --only-binary :all: cryptography
pip install --only-binary :all: passlib[bcrypt]
pip install -r requirements.txt
```

## Alternative: Install without bcrypt (if wheels aren't available)

If the above doesn't work, you can use passlib without bcrypt:

```powershell
# Install passlib without bcrypt
pip install passlib

# Then manually install bcrypt if available as wheel
pip install --only-binary :all: bcrypt
```

## Verify Installation

```powershell
python -c "import passlib; import bcrypt; print('Success!')"
```

