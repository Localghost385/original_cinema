import { fail, redirect } from '@sveltejs/kit';
import type { Actions, PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ locals: { safeGetSession } }) => {
	const { session } = await safeGetSession();

	// If the user is already logged in, redirect to the account page
	if (session) {
		throw redirect(303, '/account');
	}
};

export const actions: Actions = {
	default: async ({ request, locals: { supabase } }) => {
		const formData = await request.formData();
		const firstName = formData.get('first_name') as string;
		const lastName = formData.get('last_name') as string;
		const email = formData.get('email') as string;
		const password = formData.get('password') as string;

		// Validate email format
		const validEmail = /^[\w-\.+]+@([\w-]+\.)+[\w-]{2,8}$/.test(email);
		if (!validEmail) {
			return fail(400, { errors: { email: 'Please enter a valid email address' }, email });
		}

		// Ensure password meets basic security requirements
		if (password.length < 6) {
			return fail(400, {
				errors: { password: 'Password must be at least 6 characters long' },
				email
			});
		}

		// Attempt to create the user
		const { error } = await supabase.auth.signUp({
			email,
			password,
			options: { data: { first_name: firstName, last_name: lastName } }
		});

		if (error) {
			console.log(error);
			return fail(400, {
				success: false,
				email,
				message: 'There was an issue creating your account. Please try again.'
			});
		}

		return {
			success: true,
			message: 'Account created successfully! Please check your email for a verification link.'
		};
	}
};
