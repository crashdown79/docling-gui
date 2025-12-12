# Docling Installation Fix - No More Root Required!

## Problem Identified

The application was attempting to use a **system-wide Docling installation** located at:
```
/Library/Frameworks/Python.framework/Versions/3.12/bin/docling
```

This installation:
- Was owned by `root`
- Required root privileges to run
- Was installed globally with `sudo pip install`

Meanwhile, the virtual environment had its own **user-level Docling installation** at:
```
/Users/stefanlenz/scripts/docling-gui/venv/bin/docling
```

This installation:
- Is owned by your user account
- Runs without root privileges
- Is isolated to the virtual environment

## Solution Implemented

Updated `core/converter.py` to **automatically detect and use the virtual environment's Docling executable** instead of relying on system PATH resolution.

### What Changed:

1. **Added `_get_docling_path()` method**:
   - Detects if running in a virtual environment
   - Prioritizes venv's docling over system-wide installation
   - Falls back gracefully if venv docling not found

2. **Modified `build_command()` method**:
   - Changed from: `cmd = ["docling", input_path]`
   - Changed to: `cmd = [self.docling_path, input_path]`
   - Now uses the full path to venv's docling

3. **Enhanced console logging**:
   - Shows which docling executable is being used
   - Helps verify correct installation is active

## Verification

### Before Fix:
```bash
$ which docling
/Library/Frameworks/Python.framework/Versions/3.12/bin/docling  # ❌ Root-owned

$ ls -la /Library/Frameworks/Python.framework/Versions/3.12/bin/docling
-rwxr-xr-x  1 root  wheel  262  9 Sep. 15:41  # ❌ Owned by root
```

### After Fix:
```bash
$ ./venv/bin/python -c "from core.converter import DoclingConverter; print(DoclingConverter().docling_path)"
/Users/stefanlenz/scripts/docling-gui/venv/bin/docling  # ✅ User-owned venv version

$ ls -la /Users/stefanlenz/scripts/docling-gui/venv/bin/docling
-rwxr-xr-x  1 stefanlenz  staff  266 12 Dec. 12:37  # ✅ Owned by user
```

## How It Works Now

When you launch the GUI:

1. **Converter initializes**: `DoclingConverter.__init__()` is called
2. **Path detection**: `_get_docling_path()` runs automatically
3. **Priority order**:
   - ✅ First: Check virtual environment's `bin/docling`
   - Second: Check Python executable's directory
   - Last: Fall back to system PATH

4. **Console shows path**: GUI displays which docling is being used:
   ```
   Docling GUI initialized. Ready to convert documents.
   Using Docling: /Users/stefanlenz/scripts/docling-gui/venv/bin/docling
   ```

5. **Commands use venv**: All docling commands now use the full venv path:
   ```bash
   /Users/stefanlenz/scripts/docling-gui/venv/bin/docling input.pdf --to md --output /tmp
   ```

## Benefits

✅ **No root required**: Runs with your user permissions
✅ **Virtual environment isolation**: Uses the correct Docling version
✅ **Automatic detection**: No manual configuration needed
✅ **Clear feedback**: Console shows which docling is active
✅ **Safe execution**: Cannot accidentally modify system files

## Testing

You can verify the fix is working:

```bash
# 1. Check detected path
./venv/bin/python -c "
from core.converter import DoclingConverter
converter = DoclingConverter()
print(f'Docling path: {converter.docling_path}')
"

# Expected output:
# Docling path: /Users/stefanlenz/scripts/docling-gui/venv/bin/docling

# 2. Test command generation
./venv/bin/python -c "
from core.converter import DoclingConverter
converter = DoclingConverter()
cmd = converter.build_command(
    input_path='test.pdf',
    output_format='md',
    output_dir='/tmp',
    processing_mode='online',
    ocr_enabled=True
)
print(' '.join(cmd))
"

# Expected output:
# /Users/stefanlenz/scripts/docling-gui/venv/bin/docling test.pdf --to md --output /tmp --ocr

# 3. Launch GUI and check console
./venv/bin/python main.py
# Look in console output - should show:
# "Using Docling: /Users/stefanlenz/scripts/docling-gui/venv/bin/docling"
```

## What to Do with System Docling (Optional)

You can optionally remove the system-wide Docling installation if you're not using it elsewhere:

```bash
# Check what would be removed (safe to run)
pip3.12 show docling

# Remove if you want (requires sudo since it's system-wide)
# sudo pip3.12 uninstall docling

# Or just leave it - the GUI will ignore it and use the venv version
```

## Files Modified

1. **core/converter.py**:
   - Added `_get_docling_path()` method
   - Modified `__init__()` to call path detection
   - Updated `build_command()` to use `self.docling_path`
   - Enhanced `check_docling_installed()` for better detection

2. **ui/main_window.py**:
   - Updated `_check_docling()` to log the docling path being used
   - Provides user feedback in console

## Troubleshooting

### If you still get permission errors:

1. **Verify you're using the run script**:
   ```bash
   ./run.sh  # macOS/Linux
   run.bat   # Windows
   ```

2. **Check docling path in console**:
   - Launch GUI
   - Look at console output
   - Should show venv path, not system path

3. **Manually test venv docling**:
   ```bash
   ./venv/bin/docling --version
   # Should work without sudo
   ```

4. **Reinstall in venv if needed**:
   ```bash
   source venv/bin/activate
   pip uninstall docling -y
   pip install docling
   ```

## Summary

✅ **Problem solved**: Docling now runs with user permissions
✅ **No configuration needed**: Automatic venv detection
✅ **Clear visibility**: Console shows which docling is active
✅ **Production ready**: Safe and reliable operation

You can now use the Docling GUI without any root/sudo requirements!

---

**Fixed**: 2025-12-12
**Version**: 1.0.1 (Post-MVP Fix)
**Status**: Resolved ✅
