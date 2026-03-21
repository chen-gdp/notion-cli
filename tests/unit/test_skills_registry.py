"""Tests for the skills registry module."""

from pathlib import Path

from notion_cli.core.skills_registry import (
    SkillRegistry,
    generate_skills_md,
    get_registry,
)


class TestSkillRegistry:
    """Tests for SkillRegistry class."""

    def test_registry_initialization(self):
        """Test that registry initializes empty."""
        registry = SkillRegistry()

        assert registry.list_all() == []

    def test_register_skill(self):
        """Test registering a skill."""
        registry = SkillRegistry()

        registry.register(
            name="test_skill",
            description="A test skill",
            category="test",
            usage="notion test",
            args=[{"name": "arg1", "description": "An arg", "required": True}],
            options=[{"name": "--flag", "description": "A flag"}],
            examples=["notion test arg1 --flag"],
        )

        assert len(registry.list_all()) == 1
        skill = registry.get("test_skill")
        assert skill["name"] == "test_skill"
        assert skill["category"] == "test"

    def test_get_existing_skill(self):
        """Test getting an existing skill."""
        registry = SkillRegistry()
        registry.register(
            name="existing",
            description="An existing skill",
            category="general",
            usage="notion existing",
            args=[],
            options=[],
            examples=[],
        )

        skill = registry.get("existing")

        assert skill is not None
        assert skill["name"] == "existing"

    def test_get_nonexistent_skill(self):
        """Test getting a skill that doesn't exist."""
        registry = SkillRegistry()

        skill = registry.get("nonexistent")

        assert skill is None

    def test_list_all_multiple_skills(self):
        """Test listing multiple skills."""
        registry = SkillRegistry()
        registry.register(
            name="skill1",
            description="First skill",
            category="cat1",
            usage="notion skill1",
            args=[],
            options=[],
            examples=[],
        )
        registry.register(
            name="skill2",
            description="Second skill",
            category="cat2",
            usage="notion skill2",
            args=[],
            options=[],
            examples=[],
        )

        skills = registry.list_all()

        assert len(skills) == 2

    def test_generate_skills_md_content(self):
        """Test generating markdown content."""
        registry = SkillRegistry()
        registry.register(
            name="test_skill",
            description="Test skill description",
            category="test",
            usage="notion test_skill",
            args=[{"name": "arg1", "description": "An argument", "required": True}],
            options=[{"name": "--json", "description": "Output as JSON"}],
            examples=["notion test_skill arg1 --json"],
        )

        content = registry.generate_skills_md()

        assert "# Notion CLI Skills" in content
        assert "test_skill" in content
        assert "Test skill description" in content
        assert "Usage:" in content

    def test_generate_skills_md_writes_file(self, tmp_path: Path):
        """Test that markdown is written to file."""
        registry = SkillRegistry()
        registry.register(
            name="test",
            description="Test",
            category="test",
            usage="notion test",
            args=[],
            options=[],
            examples=[],
        )
        output_file = tmp_path / "SKILLS.md"

        registry.generate_skills_md(output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert "test" in content

    def test_generate_skills_md_groups_by_category(self):
        """Test that skills are grouped by category."""
        registry = SkillRegistry()
        registry.register(
            name="skill1",
            description="First",
            category="alpha",
            usage="notion skill1",
            args=[],
            options=[],
            examples=[],
        )
        registry.register(
            name="skill2",
            description="Second",
            category="beta",
            usage="notion skill2",
            args=[],
            options=[],
            examples=[],
        )

        content = registry.generate_skills_md()

        assert "## Alpha" in content
        assert "## Beta" in content


class TestGetRegistry:
    """Tests for get_registry function."""

    def test_get_registry_returns_same_instance(self):
        """Test that get_registry returns singleton."""
        import notion_cli.core.skills_registry as skills_module

        skills_module._registry = None

        registry1 = get_registry()
        registry2 = get_registry()

        assert registry1 is registry2


class TestGenerateSkillsMd:
    """Tests for generate_skills_md function."""

    def test_generate_skills_md_uses_global_registry(self):
        """Test that function uses global registry."""
        import notion_cli.core.skills_registry as skills_module

        skills_module._registry = None

        content = generate_skills_md()

        assert "# Notion CLI Skills" in content
