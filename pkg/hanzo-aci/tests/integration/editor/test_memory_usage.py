"""Tests for memory usage in file editor."""

import gc
import os

import psutil
import pytest

from dev_aci.editor import file_editor

from .conftest import parse_result


def test_file_read_memory_usage(temp_file):
    """Test that reading a large file uses memory efficiently."""
    # Create a large file (9.5MB to stay under 10MB limit)
    file_size_mb = 9.5
    line_size = 100  # bytes per line approximately
    num_lines = int((file_size_mb * 1024 * 1024) // line_size)

    print(f"\nCreating test file with {num_lines} lines...")
    with open(temp_file, "w") as f:
        for i in range(num_lines):
            f.write(f"Line {i}: " + "x" * (line_size - 10) + "\n")

    actual_size = os.path.getsize(temp_file) / (1024 * 1024)
    print(f"File created, size: {actual_size:.2f} MB")

    # Force Python to release file handles and clear buffers
    gc.collect()

    # Get initial memory usage
    initial_memory = psutil.Process(os.getpid()).memory_info().rss
    print(f"Initial memory usage: {initial_memory / 1024 / 1024:.2f} MB")

    # Test reading specific lines
    try:
        result = file_editor(
            command="view",
            path=temp_file,
            view_range=[5000, 5100],  # Read 100 lines from middle
            enable_linting=False,
        )
    except Exception as e:
        print(f"\nError during file read: {str(e)}")
        raise

    # Check memory usage after reading
    current_memory = psutil.Process(os.getpid()).memory_info().rss
    memory_growth = current_memory - initial_memory
    print(
        f"Memory growth after reading 100 lines: {memory_growth / 1024 / 1024:.2f} MB"
    )

    # Memory growth should be small since we're only reading 100 lines
    # Allow for some overhead but it should be much less than file size
    # Increased to 3MB to account for chardet's memory usage
    max_growth_mb = 3  # 3MB max growth
    assert memory_growth <= max_growth_mb * 1024 * 1024, (
        f"Memory growth too high: {memory_growth / 1024 / 1024:.2f} MB "
        f"(limit: {max_growth_mb} MB)"
    )

    # Parse the JSON output
    try:
        result_json = parse_result(result)
        content = result_json["formatted_output_and_error"]
    except Exception as e:
        print(f"\nError parsing result: {str(e)}")
        print(f"Result: {result[:200]}...")
        raise

    # Extract the actual content (skip the header)
    content_start = content.find("Here's the result of running `cat -n`")
    if content_start == -1:
        print(f"\nUnexpected content format: {content[:200]}...")
        raise ValueError("Could not find expected content header")
    content_start = content.find("\n", content_start) + 1
    content = content[content_start:]

    # Verify we got the correct lines
    line_count = content.count("\n")
    assert line_count >= 99, f"Should have read at least 99 lines, got {line_count}"
    assert "Line 5000:" in content, "Should contain the first requested line"
    assert "Line 5099:" in content, "Should contain the last requested line"

    print("Test completed successfully")


def test_file_editor_memory_leak(temp_file):
    """Test to demonstrate memory growth during multiple file edits."""
    print("\nStarting memory leak test...")

    # Set memory limit to 128MB to make it more likely to catch issues
    memory_limit = 128 * 1024 * 1024  # 128MB in bytes
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_AS, (memory_limit, memory_limit))
        print("Memory limit set successfully")
    except Exception as e:
        print(f"Warning: Could not set memory limit: {str(e)}")

    initial_memory = psutil.Process(os.getpid()).memory_info().rss
    print(f"\nInitial memory usage: {initial_memory / 1024 / 1024:.2f} MB")

    # Create initial content that's large enough to test but not overwhelming
    # Keep total file size under 10MB to avoid file validation errors
    base_content = (
        "Initial content with some reasonable length to make the file larger\n"
    )
    content = base_content * 100
    print(f"\nCreating initial file with {len(content)} bytes")
    with open(temp_file, "w") as f:
        f.write(content)
    print(f"Initial file created, size: {os.path.getsize(temp_file) / 1024:.1f} KB")

    try:
        # Store memory readings for analysis
        memory_readings = []
        file_size_mb = 0

        # Perform edits with reasonable content size
        for i in range(1000):  # Increased iterations, smaller content per iteration
            # Create content for each edit - keep it small to avoid file size limits
            old_content = f"content_{i}\n" * 5  # 5 lines per edit
            new_content = f"content_{i + 1}\n" * 5

            # Instead of appending, we'll replace content to keep file size stable
            with open(temp_file, "r") as f:
                current_content = f.read()

            # Insert old_content at a random position while keeping file size stable
            insert_pos = len(current_content) // 2
            new_file_content = (
                current_content[:insert_pos]
                + old_content
                + current_content[insert_pos + len(old_content) :]
            )
            with open(temp_file, "w") as f:
                f.write(new_file_content)

            # Perform the edit
            try:
                if i == 0:
                    print(
                        f"\nInitial file size: {os.path.getsize(temp_file) / (1024 * 1024):.2f} MB"
                    )
                    print(f"Sample content to replace: {old_content[:100]}...")
                result = file_editor(
                    command="str_replace",
                    path=temp_file,
                    old_str=old_content,
                    new_str=new_content,
                    enable_linting=False,
                )
                if i == 0:
                    print(f"First edit result: {result[:200]}...")
            except Exception as e:
                print(f"\nError during edit {i}:")
                print(f"File size: {os.path.getsize(temp_file) / (1024 * 1024):.2f} MB")
                print(f"Error: {str(e)}")
                raise

            if i % 25 == 0:  # Check more frequently
                current_memory = psutil.Process(os.getpid()).memory_info().rss
                memory_mb = current_memory / 1024 / 1024
                memory_readings.append(memory_mb)

                # Get current file size
                file_size_mb = os.path.getsize(temp_file) / (1024 * 1024)

                print(f"\nIteration {i}:")
                print(f"Memory usage: {memory_mb:.2f} MB")
                print(f"File size: {file_size_mb:.2f} MB")

                # Calculate memory growth
                memory_growth = current_memory - initial_memory
                growth_percent = (memory_growth / initial_memory) * 100
                print(
                    f"Memory growth: {memory_growth / 1024 / 1024:.2f} MB ({growth_percent:.1f}%)"
                )

                # Fail if memory growth is too high
                assert memory_growth < memory_limit, (
                    f"Memory growth exceeded limit after {i} edits. "
                    f"Growth: {memory_growth / 1024 / 1024:.2f} MB"
                )

                # Check for consistent growth pattern
                if len(memory_readings) >= 3:
                    # Calculate growth rate between last 3 readings
                    growth_rate = (memory_readings[-1] - memory_readings[-3]) / 2
                    print(f"Recent growth rate: {growth_rate:.2f} MB per 50 edits")

                    # Fail if we see consistent growth above a threshold
                    # Allow more growth for initial allocations
                    max_growth = 2 if i < 100 else 1  # MB per 50 edits
                    if growth_rate > max_growth:
                        pytest.fail(
                            f"Consistent memory growth detected: {growth_rate:.2f} MB "
                            f"per 50 edits after {i} edits"
                        )

    except MemoryError:
        pytest.fail("Memory limit exceeded - possible memory leak detected")
    except Exception as e:
        if "Cannot allocate memory" in str(e):
            pytest.fail("Memory limit exceeded - possible memory leak detected")
        print(f"\nFinal file size: {file_size_mb:.2f} MB")
        raise

    # Print final statistics
    print("\nMemory usage statistics:")
    print(f"Initial memory: {memory_readings[0]:.2f} MB")
    print(f"Final memory: {memory_readings[-1]:.2f} MB")
    print(f"Total growth: {(memory_readings[-1] - memory_readings[0]):.2f} MB")
    print(f"Final file size: {file_size_mb:.2f} MB")
